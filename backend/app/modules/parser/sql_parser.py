from typing import List, Dict
import re


def extract_text(sql: str) -> str:
    """Strip SQL comments and return cleaned SQL text."""
    if not sql:
        return ""
    # remove /* */ comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    # remove -- comments
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    return sql.strip()


INJECTION_PATTERNS = [
    re.compile(r"UNION\s+SELECT", re.IGNORECASE),
    re.compile(r"DROP\s+TABLE", re.IGNORECASE),
    re.compile(r"OR\s+1\s*=\s*1", re.IGNORECASE),
    re.compile(r";\s*DROP", re.IGNORECASE),
    re.compile(r"EXEC\s*\(|xp_cmdshell", re.IGNORECASE),
]


def detect_injection(sql: str) -> List[Dict]:
    text = extract_text(sql)
    findings = []
    for pat in INJECTION_PATTERNS:
        for m in pat.finditer(text):
            match = m.group(0)
            findings.append({
                "type": "sql_injection",
                "risk": "high",
                "match": match,
                "masked_value": "[SQL_INJECTION_REDACTED]",
            })
    return findings
