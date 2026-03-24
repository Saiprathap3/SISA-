import re
from typing import List, Dict, Any

# Patterns from Section 2 Layer 1
PATTERNS: Dict[str, Dict] = {
    # Sensitive Data
    "email": {
        "pattern": re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
        "risk": "low"
    },
    "api_key": {
        "pattern": re.compile(r'(sk-[a-zA-Z0-9]{20,}|api[_-]?key\s*[=:]\s*\S+)'),
        "risk": "critical"
    },
    "password": {
        "pattern": re.compile(r'(password|passwd|pwd)\s*[=:]\s*\S+', re.IGNORECASE),
        "risk": "critical"
    },
    "bearer_token": {
        "pattern": re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*'),
        "risk": "high"
    },
    "aws_key": {
        "pattern": re.compile(r'AKIA[0-9A-Z]{16}'),
        "risk": "critical"
    },
    "jwt_token": {
        "pattern": re.compile(r'eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+'),
        "risk": "high"
    },
    "credit_card": {
        "pattern": re.compile(r'\b(?:\d[ -]?){13,16}\b'),
        "risk": "critical"
    },
    "ssn": {
        "pattern": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        "risk": "critical"
    },
    "ipv4": {
        "pattern": re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
        "risk": "low"
    },
    
    # Security Attack Patterns
    "sql_injection": {
        "pattern": re.compile(r"('|\"|\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|OR\s+1=1|AND\s+1=1)\b)", re.IGNORECASE),
        "risk": "high"
    },
    "xss": {
        "pattern": re.compile(r'(<script|javascript:|onerror=|onload=)', re.IGNORECASE),
        "risk": "high"
    },
    "path_traversal": {
        "pattern": re.compile(r'(\.\./|\.\.\\|%2e%2e%2f)', re.IGNORECASE),
        "risk": "high"
    },
    "command_injection": {
        "pattern": re.compile(r'(;|\||&&|\$\(|`)'),
        "risk": "high"
    },
    "log4shell": {
        "pattern": re.compile(r'\$\{jndi:', re.IGNORECASE),
        "risk": "critical"
    }
}

def detect_all(text: str) -> List[Dict[str, Any]]:
    """Detect all patterns in a text string.
    Returns list of dicts: {type, risk, match, line_no=None, masked_value=None}
    """
    if not text:
        return []
    
    findings = []
    for f_type, meta in PATTERNS.items():
        for m in meta["pattern"].finditer(text):
            findings.append({
                "type": f_type,
                "risk": meta["risk"],
                "match": m.group(0),
                "line_no": None,
                "masked_value": None
            })
    return findings

def detect_in_lines(lines: List[str]) -> List[Dict[str, Any]]:
    """Detect patterns in a list of string lines."""
    findings = []
    for i, line in enumerate(lines, 1):
        for f_type, meta in PATTERNS.items():
            for m in meta["pattern"].finditer(line):
                findings.append({
                    "type": f_type,
                    "risk": meta["risk"],
                    "match": m.group(0),
                    "line": i,
                    "original_line": line
                })
    return findings
