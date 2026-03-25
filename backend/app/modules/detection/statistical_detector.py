import re
import math
from typing import List, Dict
from collections import Counter


def shannon_entropy(s: str) -> float:
    """Calculate Shannon entropy of a string"""
    if not s or len(s) < 2:
        return 0.0
    freq = Counter(s)
    length = len(s)
    return -sum(
        (count / length) * math.log2(count / length)
        for count in freq.values()
    )


def detect_statistical_anomalies(text: str, content_type: str = "text") -> List[Dict]:
    """
    Statistical anomaly detection — runs on ALL input types.
    Detects: high entropy strings, repeated failures, 
    encoded payloads, IP anomalies.
    """
    findings = []
    lines = text.strip().replace('\r\n', '\n').split('\n')

    # 1. High entropy strings → likely secrets/keys
    seen_tokens = set()
    for line_num, line in enumerate(lines, start=1):
        tokens = re.findall(r'[A-Za-z0-9+/=_\-]{8,}', line)
        for token in tokens:
            if token in seen_tokens:
                continue
            seen_tokens.add(token)
            entropy = shannon_entropy(token)
            if entropy > 4.2 and len(token) >= 12:
                findings.append({
                    "type": "high_entropy_string",
                    "risk": "high",
                    "category": "statistical",
                    "match": token[:25] + ("..." if len(token) > 25 else ""),
                    "line": line_num,
                    "detail": f"Entropy {entropy:.2f} — likely encoded secret or key",
                    "detection_method": "statistical"
                })

    # 2. Repeated failure patterns (brute-force indicator)
    failure_keywords = [
        "failed", "failure", "invalid", "unauthorized",
        "denied", "rejected", "403", "401", "auth error"
    ]
    failure_count = sum(
        1 for line in lines
        if any(kw in line.lower() for kw in failure_keywords)
    )
    if failure_count >= 3:
        findings.append({
            "type": "repeated_failures",
            "risk": "high",
            "category": "statistical",
            "match": f"{failure_count} failure patterns detected",
            "line": 1,
            "detail": f"Failure rate: {failure_count}/{len(lines)} lines — possible attack",
            "detection_method": "statistical"
        })

    # 3. Long base64-like strings → encoded payloads
    seen_payloads = set()
    for line_num, line in enumerate(lines, start=1):
        long_strings = re.findall(r'[A-Za-z0-9+/]{40,}={0,2}', line)
        for s in long_strings:
            if s[:20] in seen_payloads:
                continue
            seen_payloads.add(s[:20])
            findings.append({
                "type": "encoded_payload",
                "risk": "medium",
                "category": "statistical",
                "match": s[:30] + "...",
                "line": line_num,
                "detail": "Possible base64 encoded data — may hide sensitive content",
                "detection_method": "statistical"
            })

    # 4. Repeated IP anomaly
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    all_ips = ip_pattern.findall(text)
    ip_counts = Counter(all_ips)
    for ip, count in ip_counts.items():
        if count >= 3:
            findings.append({
                "type": "repeated_ip",
                "risk": "medium",
                "category": "statistical",
                "match": ip,
                "line": 1,
                "detail": f"IP {ip} seen {count} times — possible scanning",
                "detection_method": "statistical"
            })

    return findings
