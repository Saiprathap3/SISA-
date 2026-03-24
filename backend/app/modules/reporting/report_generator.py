import json
import csv
import io
from datetime import datetime
from typing import List, Dict, Any

def generate_json_report(results: Dict[str, Any]) -> Dict[str, Any]:
    """JSON report (primary API response)."""
    # Assuming results contains all fields gathered from all detection layers
    report = {
        "summary": results.get("summary", "Analysis complete"),
        "content_type": results.get("content_type", "log"),
        "total_lines_analyzed": results.get("total_lines", 0),
        "findings": results.get("findings", []),
        "risk_score": results.get("risk_score", 0),
        "risk_level": results.get("risk_level", "LOW"),
        "action": results.get("action", "allowed"),
        "insights": results.get("insights", []),
        "detection_breakdown": results.get("detection_breakdown", {
            "regex_findings": 0,
            "statistical_findings": 0,
            "ml_findings": 0,
            "ai_findings": 0
        }),
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    return report

def generate_csv_export(findings: List[Dict[str, Any]]) -> str:
    """CSV export for hackathon evaluators."""
    output = io.StringIO()
    # Columns: line_number, finding_type, risk_level, detection_method, masked_value, recommendation
    writer = csv.DictWriter(output, fieldnames=[
        "line_number", "finding_type", "risk_level", "detection_method", "masked_value", "recommendation"
    ])
    writer.writeheader()
    for f in findings:
        writer.writerow({
            "line_number": f.get("line", "-"),
            "finding_type": f.get("type", "unknown"),
            "risk_level": f.get("risk", "LOW"),
            "detection_method": f.get("detection_method", "regex"),
            "masked_value": f.get("value", "[SENSITIVE]"),
            "recommendation": f.get("recommendation", "Review log entry")
        })
    return output.getvalue()

def generate_plain_text_alerts(results: Dict[str, Any]) -> str:
    """Plain text alerts summary."""
    findings = results.get("findings", [])
    text = f"=== SECUREAI ANALYSIS REPORT ===\n"
    text += f"Risk Level: {results.get('risk_level', 'LOW')}\n"
    text += f"Total Findings: {len(findings)}\n"
    
    for f in findings:
        risk = f.get("risk", "LOW").upper()
        line = f.get("line", "-") or "-"
        ft_type = f.get("type", "unknown").replace("_", " ").title()
        val = f.get("value", "[MASKED]")
        text += f"[{risk}] Line {line} — {ft_type} (value={val})\n"
        
    text += f"\nRecommendation: Review findings and secure assets."
    return text
