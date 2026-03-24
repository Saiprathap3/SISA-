import asyncio
import time
from typing import List, Dict, Any
from app.modules.detection import regex_engine
from app.modules.risk import risk_engine
from app.modules.ai import claude_gateway


async def analyze_log(lines: List[Dict[str, Any]], options: Dict[str, Any]) -> Dict[str, Any]:
    """Full pipeline for log analysis.

    - lines: list of {line_no, content, raw}
    - options: dict with keys use_ai, mask_output, block_on_critical
    Returns dict compatible with AnalyzeResponse fields.
    """
    start = time.time()
    text_lines = [l.get("content", "") for l in lines]

    # Step 1: regex detection
    findings_raw = regex_engine.detect_in_lines(text_lines)
    findings = []
    for f in findings_raw:
        findings.append({
            "type": f["type"],
            "risk": f["risk"],
            "line": f.get("line_no"),
            "masked_value": f.get("masked_value"),
            "original_line": text_lines[f.get("line_no") - 1] if f.get("line_no") else None,
        })

    anomalies: List[str] = []

    # Step 2: brute-force detection
    failed_patterns = ["failed login", "authentication failed", "invalid password"]
    lower_lines = [l.lower() for l in text_lines]
    # sliding window of 50 lines
    for i in range(0, max(1, len(lower_lines))):
        window = lower_lines[i : i + 50]
        count = sum(1 for w in window for p in failed_patterns if p in w)
        if count >= 5:
            anomalies.append(f"Brute force detected: {count} failed logins in lines {i+1}-{i+50}")
            break

    # simple repeated error detection: count ERROR occurrences
    error_count = sum(1 for l in lower_lines if "error" in l)
    if error_count > 10:
        anomalies.append(f"High error frequency: {error_count} errors in log")

    insights: List[str] = []

    # Step 3: optional AI enrichment
    ai_used = False
    if options.get("use_ai"):
        try:
            ai_used = True
            ai_result = await claude_gateway.analyze_log_findings(findings, anomalies)
            insights = ai_result.get("insights", [])
            summary = ai_result.get("summary", "")
        except Exception:
            insights = []
            summary = "AI analysis unavailable"
            ai_used = False
    else:
        summary = "Regex-based analysis"

    # Step 4: risk scoring
    score = risk_engine.score_findings(findings)
    level = risk_engine.score_to_level(score)
    action = risk_engine.determine_action(level, options)

    duration_ms = (time.time() - start) * 1000.0

    return {
        "summary": summary,
        "content_type": "log",
        "findings": findings,
        "risk_score": score,
        "risk_level": level,
        "action": action,
        "insights": insights,
        "anomalies": anomalies,
        "ai_used": ai_used,
        "request_id": "",
        "duration_ms": duration_ms,
    }
from typing import List, Dict, Any
import re
import time
from app.modules.detection import regex_engine
from app.utils.masking import mask_finding
from app.utils.logger import logger


FAILED_LOGIN_RE = re.compile(r"failed\s+login|failed authentication|invalid password|authentication failed", re.IGNORECASE)
IP_RE = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")


async def analyze_log(lines: List[Dict[str, Any]], options: Dict[str, Any]) -> Dict[str, Any]:
    """Full analysis pipeline for parsed log lines.

    `lines` is a list of dicts produced by `parse_log` with keys: line_no, content, raw.
    `options` is a dict with boolean keys: use_ai, mask_output, block_on_critical.
    Returns a dict compatible with `AnalyzeResponse` fields (subset used by tests).
    """
    start = time.time()
    findings: List[Dict[str, Any]] = []
    anomalies: List[str] = []
    insights: List[str] = []

    # Step 1: regex detection per line
    texts = [l["content"] for l in lines]
    detected = regex_engine.detect_in_lines(texts)
    for d in detected:
        line_no = d.get("line_no")
        match = d.get("match")
        ftype = d.get("type")
        risk = d.get("risk")
        masked_line = mask_finding(lines[line_no - 1]["content"], ftype, match) if line_no and match else lines[line_no - 1]["content"]
        findings.append({
            "type": ftype,
            "risk": risk,
            "line": line_no,
            "masked_value": masked_line,
            "original_line": lines[line_no - 1]["raw"] if line_no else None,
        })

    # Step 2: brute force detection
    failed_positions = [l["line_no"] for l in lines if FAILED_LOGIN_RE.search(l.get("content", ""))]
    if failed_positions:
        for i, pos in enumerate(failed_positions):
            window = [p for p in failed_positions if 0 <= p - pos < 50]
            if len(window) >= 5:
                anomalies.append(f"Brute force detected: {len(window)} failed logins starting at line {pos}")
                break

    # repeated failed auth by IP
    ip_counts: Dict[str, int] = {}
    for l in lines:
        m = IP_RE.search(l.get("content", ""))
        if m and FAILED_LOGIN_RE.search(l.get("content", "")):
            ip = m.group(0)
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
    for ip, count in ip_counts.items():
        if count >= 3:
            anomalies.append(f"Repeated failed auth from IP {ip}: {count} times")

    # Step 3: AI analysis (optional)
    ai_used = False
    summary = "Regex-only analysis"
    if options.get("use_ai"):
        try:
            from app.modules.ai.claude_gateway import ClaudeGateway

            gw = ClaudeGateway()
            # prepare lightweight findings for AI
            findings_json = [{"type": f["type"], "risk": f["risk"], "line": f["line"]} for f in findings]
            ai_resp = await gw.analyze_log_findings(findings_json, anomalies)
            if ai_resp and ai_resp.get("insights"):
                ai_used = True
                insights.extend(ai_resp.get("insights", []))
                summary = ai_resp.get("summary", summary)
        except Exception:
            logger.info("AI gateway unavailable; continuing with regex-only analysis")

    # Step 4: risk scoring & policy
    from app.modules.risk.risk_scorer import compute_risk
    from app.modules.policy.policy_engine import evaluate

    score, level, action = compute_risk(findings, options)

    decision = evaluate(findings, anomalies, options)
    # ensure action from policy takes precedence
    action = decision.action

    duration_ms = (time.time() - start) * 1000.0

    return {
        "summary": summary,
        "content_type": "logs",
        "findings": findings,
        "risk_score": score,
        "risk_level": level,
        "action": action,
        "insights": insights,
        "anomalies": anomalies,
        "ai_used": ai_used,
        "request_id": "",
        "duration_ms": duration_ms,
    }
