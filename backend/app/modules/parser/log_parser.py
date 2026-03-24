import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Apache/Nginx (Common/Combined Log Format)
APACHE_PATTERN = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>.*?)\] '
    r'"(?P<method>\w+) (?P<path>.*?) HTTP/.*?" '
    r'(?P<status>\d+) (?P<size>\d+)'
)

# /var/log/auth.log format (simplified)
# Example: Mar 24 23:10:01 user sshd[1234]: Failed password for invalid user admin from 1.2.3.4 port 1234 ssh2
AUTH_LOG_PATTERN = re.compile(
    r'(?P<timestamp>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+(?P<host>\S+)\s+(?P<process>\S+):\s+(?P<message>.*)'
)

# key=value pattern
KV_PATTERN = re.compile(r'(?P<key>\w+)=(?P<value>\S+)')

# Status Code Map
STATUS_RISK_MAP = {
    '5': 'medium',  # 5xx
    '4': 'low-medium', # 4xx
    '401': 'high',
    '403': 'high'
}

def normalize_timestamp(raw_ts: str) -> str:
    # Basic normalization to ISO 8601
    # Example Apache: 24/Mar/2026:23:10:00 +0000
    try:
        # Common Apache format
        dt = datetime.strptime(raw_ts.split(' ')[0], "%d/%b/%Y:%H:%M:%S")
        return dt.isoformat()
    except Exception:
        return raw_ts

def detect_format(lines: List[str]) -> str:
    """Scan first 5 lines to detect log format."""
    sample = lines[:5]
    if any(l.strip().startswith('{') for l in sample):
        return 'json'
    if any(APACHE_PATTERN.match(l) for l in sample):
        return 'apache'
    if any(AUTH_LOG_PATTERN.match(l) for l in sample):
        return 'auth'
    if any('=' in l for l in sample):
        return 'kv'
    return 'raw'

def parse_line(line: str, line_no: int, fmt: str) -> Dict[str, Any]:
    """Parse a single line based on format and enrich."""
    log_entry = {
        "line_no": line_no,
        "content": line,
        "raw": line,
        "extra": {}
    }

    if fmt == 'json':
        try:
            data = json.loads(line)
            log_entry["extra"].update(data)
        except Exception:
            pass
    elif fmt == 'apache':
        m = APACHE_PATTERN.match(line)
        if m:
            groups = m.groupdict()
            log_entry["extra"].update(groups)
            log_entry["extra"]["timestamp"] = normalize_timestamp(groups.get("timestamp", ""))
    elif fmt == 'auth':
        m = AUTH_LOG_PATTERN.match(line)
        if m:
            log_entry["extra"].update(m.groupdict())
    elif fmt == 'kv':
        matches = KV_PATTERN.findall(line)
        for k, v in matches:
            log_entry["extra"][k] = v

    # Status Risk Mapping
    status = str(log_entry["extra"].get("status", ""))
    if status == "401" or status == "403":
        log_entry["base_risk"] = "high"
    elif status.startswith("5"):
        log_entry["base_risk"] = "medium"
    elif status.startswith("4"):
        log_entry["base_risk"] = "low-medium"
    else:
        log_entry["base_risk"] = "low"

    return log_entry

def parse_log(content: str) -> List[Dict[str, Any]]:
    """Parse log string with auto-detection and enrichment."""
    if not content:
        return []
    
    # Handle \r\n and \n
    lines = content.splitlines()
    fmt = detect_format(lines)
    
    results = []
    for i, line in enumerate(lines, 1):
        if not line.strip(): # Skip empty
            continue
        try:
            parsed = parse_line(line, i, fmt)
            results.append(parsed)
        except Exception:
            # Skip malformed without crashing
            continue
            
    return results
