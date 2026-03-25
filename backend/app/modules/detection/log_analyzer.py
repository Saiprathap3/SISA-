import re
from typing import List, Dict
from app.modules.detection.regex_engine import detect_all


def parse_log_lines(text: str) -> List[str]:
    """Handle both Unix and Windows line endings"""
    return text.replace('\r\n', '\n').replace('\r', '\n').split('\n')


def detect_brute_force(lines: List[str]) -> List[Dict]:
    """
    Detect brute force: 5+ failed login attempts = HIGH risk.
    Spec requirement: detect repeated failures.
    """
    findings = []
    failed_keywords = [
        "failed login", "login failed", "failed attempt",
        "authentication failed", "invalid password", "invalid credentials",
        "auth failed", "incorrect password", "wrong password",
        "failed password", "invalid user"
    ]
    
    failed_lines = []
    for i, line in enumerate(lines, start=1):
        line_lower = line.lower()
        if any(kw in line_lower for kw in failed_keywords):
            failed_lines.append(i)

    if len(failed_lines) >= 5:
        findings.append({
            "type": "brute_force",
            "risk": "high",
            "category": "statistical",
            "match": f"{len(failed_lines)} failed login attempts detected",
            "line": failed_lines[0],
            "value": "[ANOMALY: BRUTE FORCE DETECTED]",
            "detail": f"Failed login attempts at lines: {failed_lines[:5]}",
            "detection_method": "statistical"
        })

    return findings


def detect_suspicious_ip(lines: List[str]) -> List[Dict]:
    """
    Spec requirement 4.3: Suspicious IP activity detection.
    """
    findings = []
    ip_pattern = re.compile(
        r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
        r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
    )
    from collections import Counter
    ip_lines = {}
    
    for i, line in enumerate(lines, start=1):
        ips = ip_pattern.findall(line)
        for ip in ips:
            if ip not in ip_lines:
                ip_lines[ip] = []
            ip_lines[ip].append(i)

    for ip, line_nums in ip_lines.items():
        if len(line_nums) >= 3:
            findings.append({
                "type": "suspicious_ip_activity",
                "risk": "medium",
                "category": "statistical",
                "match": ip,
                "line": line_nums[0],
                "detail": f"IP {ip} appears on {len(line_nums)} lines: {line_nums[:3]}",
                "detection_method": "statistical"
            })

    return findings


def detect_debug_leak(lines: List[str]) -> List[Dict]:
    """
    Spec requirement 4.3: Debug mode leaks.
    """
    findings = []
    debug_patterns = [
        "debug=true", "debug mode", "verbose=true",
        "stacktrace", "stack_trace", "internal server error",
        "at com.", "at java.", "at org.", "at sun."
    ]
    for i, line in enumerate(lines, start=1):
        line_lower = line.lower()
        if any(p in line_lower for p in debug_patterns):
            findings.append({
                "type": "debug_leak",
                "risk": "medium",
                "category": "leak",
                "match": line.strip()[:80],
                "line": i,
                "detail": "Debug information leaked — disable in production",
                "detection_method": "statistical"
            })

    return findings


def analyze_log(text: str) -> Dict:
    """
    Main log analysis function.
    Spec section 3.3 — runs full detection pipeline on log content.
    Returns findings + line count for API response.
    """
    lines = parse_log_lines(text)
    non_empty_lines = [l for l in lines if l.strip()]

    # Layer 1: Regex detection on all lines
    regex_findings = detect_all(text)

    # Layer 2: Statistical / log-specific detection
    statistical_findings = []
    statistical_findings.extend(detect_brute_force(non_empty_lines))
    statistical_findings.extend(detect_suspicious_ip(non_empty_lines))
    statistical_findings.extend(detect_debug_leak(non_empty_lines))

    all_findings = regex_findings + statistical_findings

    return {
        "findings": all_findings,
        "total_lines": len(non_empty_lines),
        "regex_count": len(regex_findings),
        "statistical_count": len(statistical_findings)
    }
