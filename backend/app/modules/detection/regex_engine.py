import re
from typing import List, Dict

PATTERNS = {
    "email": {
        "regex": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        "risk": "low",
        "category": "pii"
    },
    "password": {
        # Matches: password=x, password:x, password is x, pass=x
        "regex": r"(?i)(password|passwd|pwd|pass)\s*(?:is\s+|=\s*|:\s*)\S+",
        "risk": "critical",
        "category": "credential"
    },
    "api_key": {
        # Matches: api_key=x, apikey=x, api key is x, sk-xxxx, AKIA...
        "regex": r"(?i)(api[_\-]?key|apikey)\s*(?:is\s+|=\s*|:\s*)\S+|sk-[a-zA-Z0-9]{10,}|AKIA[0-9A-Z]{16}",
        "risk": "high",
        "category": "credential"
    },
    "secret": {
        "regex": r"(?i)(secret|private[_\-]?key|client[_\-]?secret|app[_\-]?secret)\s*(?:=\s*|:\s*)\S+",
        "risk": "critical",
        "category": "credential"
    },
    "hardcoded_secret": {
        "regex": r"(?i)(auth[_\-]?secret|encryption[_\-]?key|signing[_\-]?key)\s*(?:=\s*|:\s*)\S+",
        "risk": "critical",
        "category": "credential"
    },
    "bearer_token": {
        "regex": r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]{10,}=*",
        "risk": "high",
        "category": "credential"
    },
    "token": {
        "regex": r"(?i)(token|auth[_\-]?token|access[_\-]?token|refresh[_\-]?token)\s*(?:=\s*|:\s*)\S+",
        "risk": "high",
        "category": "credential"
    },
    "phone": {
        "regex": r"(\+?1?\s?)?(\(?\d{3}\)?[\s\-\.]?)(\d{3}[\s\-\.]?\d{4})",
        "risk": "low",
        "category": "pii"
    },
    "stack_trace": {
        "regex": r"(?i)(exception|traceback|nullpointerexception|stack\s*trace|error\s+at\s+\w+\.\w+:\d+)",
        "risk": "medium",
        "category": "leak"
    },
    "sql_injection": {
        "regex": r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE|EXEC|EXECUTE)\b",
        "risk": "high",
        "category": "injection"
    },
    "command_injection": {
        "regex": r"(;|\||&&|\$\(|`|>\s*/|<\s*/)",
        "risk": "high",
        "category": "injection"
    },
    "ip_address": {
        "regex": r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b",
        "risk": "low",
        "category": "network"
    },
    "debug_mode": {
        "regex": r"(?i)(debug\s*=\s*true|debug\s*mode\s*(on|enabled)|verbose\s*=\s*true)",
        "risk": "medium",
        "category": "leak"
    },
    "jwt_token": {
        "regex": r"eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+",
        "risk": "high",
        "category": "credential"
    },
    "aws_key": {
        "regex": r"AKIA[0-9A-Z]{16}",
        "risk": "critical",
        "category": "credential"
    },
    "credit_card": {
        "regex": r"\b(?:\d[ \-]?){13,16}\b",
        "risk": "high",
        "category": "pii"
    }
}


def detect_all(text: str) -> List[Dict]:
    """
    Run all regex patterns against text line by line.
    Always returns line numbers. Works for ALL input types.
    """
    findings = []
    lines = text.split('\n')

    for line_num, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        for pattern_name, pattern_data in PATTERNS.items():
            try:
                matches = re.finditer(
                    pattern_data["regex"], line, re.IGNORECASE
                )
                for match in matches:
                    findings.append({
                        "type": pattern_name,
                        "risk": pattern_data["risk"],
                        "category": pattern_data["category"],
                        "match": match.group(),
                        "line": line_num,
                        "start": match.start(),
                        "end": match.end(),
                        "detection_method": "regex"
                    })
            except re.error:
                continue  # Never crash on bad regex

    return findings


def get_all_patterns() -> Dict:
    """Return patterns metadata for /patterns endpoint"""
    return {
        name: {
            "risk": data["risk"],
            "category": data["category"]
        }
        for name, data in PATTERNS.items()
    }
