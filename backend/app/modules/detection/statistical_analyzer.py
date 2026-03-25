from typing import List, Dict, Any
from datetime import datetime, timedelta

# Patterns for failed login
FAILED_PATTERNS = [
    "failed login",
    "login failed",
    "failed attempt",
    "authentication failed",
    "invalid password",
    "FAILED login",
    "Failed password",
    "authentication failure",
    "Invalid user"
]

# Patterns for privilege escalation
PRIV_ESC_PATTERNS = [
    ("sudo:", "command not allowed"),
    ("su:", "FAILED"),
    "user not in sudoers"
]

def detect_brute_force(parsed_lines: List[Dict[str, Any]], threshold=5, window_seconds=30) -> List[Dict[str, Any]]:
    """Track failed login attempts per IP within a window, or count sequentially if no IP available."""
    failures_by_ip: Dict[str, List[datetime]] = {}
    anomalies = []
    failed_count = 0
    
    for i, entry in enumerate(parsed_lines):
        content = entry.get("content", "").lower()
        ip = entry.get("extra", {}).get("ip") or entry.get("extra", {}).get("host")
        
        is_failure = any(p.lower() in content for p in FAILED_PATTERNS)
        
        if is_failure:
            if ip:
                # Track by IP if available
                ts_str = entry.get("extra", {}).get("timestamp")
                try:
                    ts = datetime.fromisoformat(ts_str) if ts_str else datetime.now()
                except Exception:
                    ts = datetime.now()
                    
                if ip not in failures_by_ip:
                    failures_by_ip[ip] = []
                failures_by_ip[ip].append(ts)
                
                # Check window
                window_start = ts - timedelta(seconds=window_seconds)
                recent_failures = [f for f in failures_by_ip[ip] if f >= window_start]
                failures_by_ip[ip] = recent_failures # prune old ones
                
                if len(recent_failures) >= threshold:
                    anomalies.append({
                        "ip": ip,
                        "attempt_count": len(recent_failures),
                        "time_window": f"{window_seconds}s",
                        "risk": "critical",
                        "type": "brute_force_attack"
                    })
                    # Once flagged, clear for that IP to avoid double flagging every line
                    failures_by_ip[ip] = []
            else:
                # No IP available - count sequentially
                failed_count += 1
                if failed_count >= threshold:
                    anomalies.append({
                        "attempt_count": failed_count,
                        "risk": "critical",
                        "type": "brute_force_attack",
                        "line": i + 1,
                        "message": f"{failed_count} failed login attempts detected"
                    })
                    # Reset after detection
                    failed_count = 0
                
    return anomalies

def detect_privilege_escalation(parsed_lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Match privilege escalation patterns."""
    findings = []
    for entry in parsed_lines:
        content = entry.get("content", "")
        line_no = entry.get("line_no")
        
        is_priv_esc = False
        for p in PRIV_ESC_PATTERNS:
            if isinstance(p, tuple):
                if all(sub.lower() in content.lower() for sub in p):
                    is_priv_esc = True
                    break
            else:
                if p.lower() in content.lower():
                    is_priv_esc = True
                    break
                    
        if is_priv_esc:
            findings.append({
                "type": "privilege_escalation",
                "risk": "high",
                "line": line_no,
                "user": entry.get("extra", {}).get("user"),
                "command": entry.get("extra", {}).get("command") or content
            })
    return findings

def detect_repeated_errors(parsed_lines: List[Dict[str, Any]], threshold=10) -> List[Dict[str, Any]]:
    """Count 5xx errors per IP."""
    error_counts: Dict[str, int] = {}
    anomalies = []
    
    for entry in parsed_lines:
        status = str(entry.get("extra", {}).get("status", ""))
        ip = entry.get("extra", {}).get("ip")
        
        if ip and status.startswith("5"):
            error_counts[ip] = error_counts.get(ip, 0) + 1
            if error_counts[ip] >= threshold:
                anomalies.append({
                    "type": "repeated_system_errors",
                    "risk": "medium",
                    "ip": ip,
                    "error_count": error_counts[ip]
                })
                # Reset
                error_counts[ip] = 0
                
    return anomalies
