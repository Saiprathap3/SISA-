from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import os

from app.modules.detection.regex_engine import detect_all, get_all_patterns
from app.modules.detection.statistical_detector import detect_statistical_anomalies
from app.modules.detection.ml_detector import detect_ml_anomalies
from app.modules.detection.log_analyzer import analyze_log
from app.modules.risk.risk_engine import (
    calculate_risk_score, get_risk_level, get_risk_summary
)
from app.modules.policy.policy_engine import determine_action, apply_masking
from app.modules.ai.claude_gateway import get_ai_insights

router = APIRouter()
security = HTTPBearer(auto_error=False)


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Optional bearer token auth — skip if no token configured"""
    configured = os.getenv("API_BEARER_TOKEN", "")
    if configured and configured != "changeme":
        if (not credentials or 
                credentials.credentials != configured):
            raise HTTPException(
                status_code=401, 
                detail="Invalid or missing bearer token"
            )


class AnalyzeOptions(BaseModel):
    mask: bool = True
    block_high_risk: bool = True
    log_analysis: bool = True
    use_ai: bool = True


class AnalyzeRequest(BaseModel):
    input_type: str = Field(
        ..., 
        pattern="^(text|file|sql|chat|log)$",
        description="One of: text, file, sql, chat, log"
    )
    content: str = Field(..., min_length=1, max_length=500000)
    options: AnalyzeOptions = AnalyzeOptions()


@router.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    _token = Depends(verify_token)
):
    """
    Main analysis endpoint.
    Runs: Regex → Statistical → ML → AI → Risk → Policy
    Matches official project spec API contract exactly.
    """
    content = request.content.strip()
    input_type = request.input_type
    options = request.options.dict()

    # ── Step 1: Detection ──────────────────────────────────────
    
    if input_type == "log" and options.get("log_analysis", True):
        # Log-specific pipeline (spec section 3.3)
        log_result = analyze_log(content)
        regex_findings = [
            f for f in log_result["findings"] 
            if f.get("detection_method") == "regex"
        ]
        statistical_findings = [
            f for f in log_result["findings"] 
            if f.get("detection_method") == "statistical"
        ]
        total_lines = log_result["total_lines"]
    else:
        # Universal pipeline for text/file/sql/chat
        regex_findings = detect_all(content)
        statistical_findings = detect_statistical_anomalies(
            content, input_type
        )
        total_lines = len([l for l in content.split('\n') if l.strip()])

    # ML detection runs on all input types
    all_so_far = regex_findings + statistical_findings
    ml_findings = detect_ml_anomalies(content, all_so_far)

    all_findings = all_so_far + ml_findings

    # ── Step 2: Risk Engine ────────────────────────────────────
    risk_score = calculate_risk_score(all_findings)
    risk_level = get_risk_level(risk_score)
    summary = get_risk_summary(all_findings, input_type)

    # ── Step 3: AI Insights (Claude only) ─────────────────────
    ai_insights = []
    ai_findings_count = 0
    if options.get("use_ai", True) and all_findings:
        ai_insights = await get_ai_insights(
            findings=all_findings,
            content_type=input_type,
            raw_content=content[:2000]  # limit context
        )
        # Count as AI findings only if real Claude response
        is_fallback = (
            not ai_insights or 
            any(phrase in ai_insights[0].lower() 
                for phrase in ["unavailable", "appears secure", "review all"])
        )
        ai_findings_count = len(ai_insights) if not is_fallback else 0
    elif not all_findings:
        ai_insights = ["No sensitive data detected. Content appears secure."]

    # ── Step 4: Policy Engine ──────────────────────────────────
    action = determine_action(risk_level, options)
    masked_findings = apply_masking(all_findings, options.get("mask", True))

    # ── Step 5: Build Response (exact spec format) ─────────────
    return {
        "summary": summary,
        "content_type": input_type,
        "total_lines_analyzed": total_lines,
        "findings": masked_findings,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "action": action,
        "insights": ai_insights,
        "detection_breakdown": {
            "regex": len(regex_findings),
            "statistical": len(statistical_findings),
            "ml": len(ml_findings),
            "ai": ai_findings_count
        },
        "generated_at": datetime.now(timezone.utc).isoformat()
    }


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": "claude-sonnet-4-6",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/patterns")
async def patterns():
    """Return all detection patterns and their risk levels"""
    return {
        "patterns": get_all_patterns(),
        "total": len(get_all_patterns())
    }

        
    parsed = await file_parser.parse_file(file.filename, content)
    text = parsed.get("content", "")
    req = AnalyzeRequest(input_type="file", content=text, options=opts)
    return await analyze_route(req, request)
