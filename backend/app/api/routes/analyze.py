import time
import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request

from app.core.config import settings
from app.models.request_models import AnalyzeRequest
from app.modules.parser import log_parser, text_parser, sql_parser, chat_parser, file_parser
from app.modules.detection import regex_engine, statistical_analyzer, ml_analyzer
from app.modules.ai.claude_gateway import ClaudeGateway
from app.modules.risk import risk_engine
from app.modules.reporting import report_generator
from app.utils.logger import logger

router = APIRouter()

@router.post("/analyze")
async def analyze_route(req: AnalyzeRequest, request: Request):
    """Refactored analyze route with multiple detection layers and hardening."""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    start = time.time()
    
    # Section 5: Internal Logging
    logger.info("analyze request", extra={"request_id": request_id, "input_type": input_type, "content_len": len(content)})
    
    # Section 5: Generic error responses with IDs
    try:
        input_type = req.input_type
        content = req.content or ""
        options = req.options.model_dump() if hasattr(req.options, "model_dump") else (req.options or {})
        
        # Section 5: Input Validation
        if len(content) > settings.MAX_TEXT_CHARS:
             raise HTTPException(status_code=400, detail=f"Input exceeds maximum allowed length of {settings.MAX_TEXT_CHARS} chars.")

        # Handle logs vs non-logs
        all_findings = []
        anomalies = []
        ai_insights = []
        
        if input_type == "log":
            parsed_lines = log_parser.parse_log(content)
            
            # Layer 1: Regex
            regex_findings = regex_engine.detect_in_lines([l["content"] for l in parsed_lines])
            all_findings.extend(regex_findings)
            
            # Layer 2: Statistical
            stats_anomalies = statistical_analyzer.detect_brute_force(parsed_lines)
            stats_findings = statistical_analyzer.detect_privilege_escalation(parsed_lines)
            all_findings.extend(stats_findings)
            anomalies.extend([s["type"] for s in stats_anomalies])
            
            # Layer 3: ML Anomaly detection
            if settings.ENABLE_ML:
                ml_anomalies = ml_analyzer.detect_ml_anomlies(parsed_lines)
                anomalies.extend([m["type"] for m in ml_anomalies])
            else:
                ml_anomalies = []
                
            # Layer 4: AI Analysis (Upgraded)
            ai_findings = []
            if options.get("use_ai"):
                # Only call if we have findings or anomalies
                if all_findings or anomalies:
                    gw = ClaudeGateway()
                    ai_result = await gw.analyze_suspicious_lines(parsed_lines)
                    ai_findings = ai_result.get("findings", [])
                    ai_insights = [ai_result.get("summary", "")] if ai_result.get("summary") else []
                    
                    # Merge AI findings into all_findings
                    for aif in ai_findings:
                        all_findings.append({
                            "line": aif.get("line"),
                            "type": aif.get("attack_type"),
                            "risk": aif.get("severity"),
                            "recommendation": aif.get("action"),
                            "detection_method": "ai",
                            "value": aif.get("asset")
                        })

            # Section 3: Risk Scoring & Policy
            score, level = risk_engine.calculate_risk_score(all_findings, ml_anomalies, ai_findings)
            action = risk_engine.enforce_policy(level, all_findings, options)
            
            # Form final response data
            results = {
                "summary": "Log analysis complete",
                "content_type": "log",
                "total_lines": len(parsed_lines),
                "findings": all_findings,
                "risk_score": score,
                "risk_level": level,
                "action": action,
                "insights": ai_insights,
                "detection_breakdown": {
                    "regex_findings": len(regex_findings),
                    "statistical_findings": len(stats_findings) + len(stats_anomalies),
                    "ml_findings": len(ml_anomalies),
                    "ai_findings": len(ai_findings)
                }
            }
            return report_generator.generate_json_report(results)

        else:
            # Simple text/sql analysis (brief implementation as per contract)
            findings = regex_engine.detect_all(content)
            score, level = risk_engine.calculate_risk_score(findings, [], [])
            action = risk_engine.enforce_policy(level, findings, options)
            
            results = {
                "summary": "Text analysis complete",
                "content_type": input_type,
                "total_lines": len(content.splitlines()),
                "findings": findings,
                "risk_score": score,
                "risk_level": level,
                "action": action,
                "insights": [],
                "detection_breakdown": { "regex_findings": len(findings), "statistical_findings": 0, "ml_findings": 0, "ai_findings": 0 }
            }
            return report_generator.generate_json_report(results)
            
    except HTTPException:
        raise
    except Exception as e:
        error_id = str(uuid.uuid4())
        logger.exception(f"Analysis failed [{error_id}]", extra={"error_id": error_id})
        raise HTTPException(status_code=500, detail={"detail": "Analysis engine error", "error_id": error_id})

@router.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...), options: str = Form(...), request: Request = None):
    """File upload route with validation."""
    import json
    
    # Section 5: Enforce MAX_FILE_SIZE_MB
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds limit of {settings.MAX_FILE_SIZE_MB}MB")

    # Mime validation
    allowed_mimes = ["text/plain", "application/pdf", "application/msword", "application/json", "text/csv"]
    if file.content_type not in allowed_mimes and not file.filename.endswith(('.txt', '.log', '.csv', '.json', '.sql')):
        raise HTTPException(status_code=415, detail="Unsupported file format")

    try:
        opts = json.loads(options)
    except Exception:
        opts = {}
        
    parsed = await file_parser.parse_file(file.filename, content)
    text = parsed.get("content", "")
    req = AnalyzeRequest(input_type="file", content=text, options=opts)
    return await analyze_route(req, request)
