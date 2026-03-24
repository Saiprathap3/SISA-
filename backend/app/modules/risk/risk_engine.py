from typing import List, Dict, Any, Tuple

# Section 3 Base Scores
BASE_SCORES = {
    "password": 40,             # password_in_log
    "api_key": 35,              # api_key_exposed
    "aws_key": 35,
    "credit_card": 35,
    "ssn": 35,
    "sql_injection": 30,
    "brute_force_attack": 25,
    "privilege_escalation": 25,
    "path_traversal": 20,
    "xss": 20,
    "bearer_token": 20,
    "jwt_token": 20,
    "stack_trace": 15,          # stack_trace_leak
    "email": 5,                 # email_exposed
    "ipv4": 2,
    "ml_anomaly_detected": 10
}

def calculate_risk_score(findings: List[Dict[str, Any]], ml_anomalies: List[Dict[str, Any]], ai_findings: List[Dict[str, Any]]) -> Tuple[int, str]:
    """Calculate weighted risk score with multipliers."""
    total_score = 0
    
    # Track repetitions
    type_counts = {}
    for f in findings:
        f_type = f.get("type", "other")
        type_counts[f_type] = type_counts.get(f_type, 0) + 1
        
        base = BASE_SCORES.get(f_type, 10)
        
        # Multiplier: Same pattern repeated 3+ times → ×1.5
        if type_counts[f_type] >= 3:
            base *= 1.5
            
        # Multiplier: ML anomaly score also triggered → ×1.3 (if IP matches)
        # Assuming findings have 'ip' if available
        ip = f.get("ip")
        if ip and any(ml.get("ip") == ip for ml in ml_anomalies):
            base *= 1.3
            
        # Multiplier: Both regex + AI flagged same line → ×2.0
        line = f.get("line")
        if line and any(ai.get("line") == line for ai in ai_findings):
            base *= 2.0
            
        total_score += int(base)

    # Statistical findings as base
    for s in ml_anomalies:
        total_score += BASE_SCORES.get(s.get("type"), 10)

    # Final levels
    if total_score >= 81:
        level = "CRITICAL"
    elif total_score >= 51:
        level = "HIGH"
    elif total_score >= 21:
        level = "MEDIUM"
    else:
        level = "LOW"
        
    return total_score, level

def mask_sensitive_value(v_type: str, value: str) -> str:
    """Mask values according to Section 3 Policy Engine."""
    if not value:
        return value
        
    if v_type == "email":
        # emails → u***@***.com
        if "@" in value:
            u, d = value.split("@", 1)
            first = u[0] if u else "u"
            return f"{first}***@***.{d.split('.')[-1] if '.' in d else 'com'}"
    elif v_type == "api_key" or v_type == "aws_key":
        # api keys → sk-***...***
        if value.startswith("sk-"):
            return f"sk-***...{value[-4:] if len(value) > 10 else ''}"
        return f"{value[:4]}***...***"
    elif v_type == "password":
        # passwords → [REDACTED]
        return "[REDACTED]"
    elif v_type == "bearer_token" or v_type == "jwt_token":
        # tokens → [TOKEN REDACTED]
        return "[TOKEN REDACTED]"
        
    return "[MASKED]"

def enforce_policy(risk_level: str, findings: List[Dict[str, Any]], options: Dict[str, Any]):
    """Apply policy: block on critical and mask if requested."""
    block_high_risk = options.get("block_on_critical", True)
    mask = options.get("mask_output", True)
    
    action = "allowed"
    
    if risk_level == "CRITICAL" and block_high_risk:
        action = "blocked"
        # Mask everything in blocked mode
        for f in findings:
            f["value"] = mask_sensitive_value(f.get("type"), f.get("match", ""))
            f["match"] = f["value"]
    elif mask:
        action = "masked"
        for f in findings:
            f["value"] = mask_sensitive_value(f.get("type"), f.get("match", ""))
            f.pop("match", None) # Remove raw match
            
    return action
