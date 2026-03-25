from typing import List, Dict


CREDENTIAL_KEYWORDS = [
    'password', 'passwd', 'secret', 'token', 'key', 'auth',
    'credential', 'private', 'bearer', 'api_key', 'access_token',
    'refresh_token', 'client_secret', 'private_key', 'encryption'
]

ATTACK_KEYWORDS = [
    'select', 'union', 'drop', 'insert', 'delete', 'exec',
    'script', 'onerror', 'onload', 'javascript:', '../', '..\\'
]


def detect_ml_anomalies(text: str, findings_so_far: List[Dict]) -> List[Dict]:
    """
    Lightweight ML-style heuristic scoring.
    No model training required.
    Detects: credential density, multi-pattern lines, long lines, attack clustering.
    """
    ml_findings = []
    lines = text.strip().replace('\r\n', '\n').split('\n')

    # Feature 1: Credential keyword density per line
    for line_num, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        line_lower = line.lower()
        hits = sum(1 for kw in CREDENTIAL_KEYWORDS if kw in line_lower)
        if hits >= 2:
            ml_findings.append({
                "type": "credential_density_anomaly",
                "risk": "high",
                "category": "ml",
                "match": f"{hits} credential keywords on line {line_num}",
                "line": line_num,
                "detail": f"ML Score: {hits * 0.3:.1f} — high concentration of sensitive terms",
                "detection_method": "ml"
            })

    # Feature 2: Multiple different finding types on same line
    line_finding_types: Dict[int, set] = {}
    for f in findings_so_far:
        ln = f.get("line", 0)
        if ln > 0:
            if ln not in line_finding_types:
                line_finding_types[ln] = set()
            line_finding_types[ln].add(f.get("type", ""))

    for line_num, types in line_finding_types.items():
        if len(types) >= 2:
            ml_findings.append({
                "type": "multi_pattern_line",
                "risk": "critical",
                "category": "ml",
                "match": f"Line {line_num}: {', '.join(sorted(types))}",
                "line": line_num,
                "detail": f"ML: {len(types)} overlapping risk patterns — high confidence threat",
                "detection_method": "ml"
            })

    # Feature 3: Anomalously long lines (data dump / injection)
    for line_num, line in enumerate(lines, start=1):
        if len(line) > 500:
            ml_findings.append({
                "type": "anomalous_line_length",
                "risk": "medium",
                "category": "ml",
                "match": f"Line {line_num}: {len(line)} chars",
                "line": line_num,
                "detail": "Unusually long line — possible data dump or injection payload",
                "detection_method": "ml"
            })

    # Feature 4: Attack keyword clustering (3+ attack keywords in same line)
    for line_num, line in enumerate(lines, start=1):
        line_lower = line.lower()
        attack_hits = sum(1 for kw in ATTACK_KEYWORDS if kw in line_lower)
        if attack_hits >= 3:
            ml_findings.append({
                "type": "attack_pattern_cluster",
                "risk": "critical",
                "category": "ml",
                "match": f"{attack_hits} attack patterns clustered on line {line_num}",
                "line": line_num,
                "detail": f"ML: Attack keyword density {attack_hits} — likely exploit attempt",
                "detection_method": "ml"
            })

    # Deduplicate by (type, line)
    seen = set()
    unique = []
    for f in ml_findings:
        key = (f["type"], f["line"])
        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique
