from typing import List, Dict

RISK_WEIGHTS = {
    "critical": 10,
    "high": 5,
    "medium": 2,
    "low": 1
}

RISK_THRESHOLDS = {
    "critical": 20,
    "high": 10,
    "medium": 4,
    "low": 0
}


def calculate_risk_score(findings: List[Dict]) -> int:
    """Calculate weighted risk score from all findings"""
    if not findings:
        return 0
    score = sum(
        RISK_WEIGHTS.get(f.get("risk", "low"), 1) 
        for f in findings
    )
    return min(score, 100)   # cap at 100


def get_risk_level(score: int) -> str:
    """Map score to risk level string"""
    if score >= RISK_THRESHOLDS["critical"]:
        return "critical"
    elif score >= RISK_THRESHOLDS["high"]:
        return "high"
    elif score >= RISK_THRESHOLDS["medium"]:
        return "medium"
    return "low"


def get_risk_summary(findings: List[Dict], content_type: str) -> str:
    """Generate human-readable summary for API response"""
    if not findings:
        return f"No sensitive data detected in {content_type} input."

    types = [f.get("type") for f in findings]
    parts = []

    if "password" in types or "secret" in types or "hardcoded_secret" in types:
        parts.append("sensitive credentials")
    if "api_key" in types or "bearer_token" in types or "token" in types:
        parts.append("exposed tokens/keys")
    if "sql_injection" in types or "command_injection" in types:
        parts.append("injection patterns")
    if "stack_trace" in types or "debug_mode" in types:
        parts.append("system information leaks")
    if "brute_force" in types or "repeated_failures" in types:
        parts.append("attack patterns")
    if "email" in types or "phone" in types:
        parts.append("PII data")

    if parts:
        return (f"{content_type.capitalize()} input contains: "
                f"{', '.join(parts)}.")
    return f"Security findings detected in {content_type} input."

