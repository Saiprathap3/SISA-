import asyncio
from typing import Dict, Any, List
from app.modules.ai import claude_gateway
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def detect(content: str | List[Dict[str, Any]], input_type: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """Call ClaudeGateway for the given input_type. Returns insights and summary.

    This function is resilient: if AI is disabled or fails, returns a safe empty result.
    """
    if not options.get("use_ai"):
        return {"insights": [], "summary": "AI skipped", "ai_used": False}
    try:
        if input_type == "log":
            findings = content if isinstance(content, list) else []
            return await claude_gateway.analyze_log_findings(findings, [])
        if input_type == "text":
            return await claude_gateway.analyze_text(str(content), [])
        if input_type == "sql":
            return await claude_gateway.analyze_sql(str(content), [])
        return {"insights": [], "summary": "AI unsupported for this type", "ai_used": False}
    except Exception as e:
        logger.info("AI detector exception", extra={"error": str(e)})
        return {"insights": [], "summary": "AI analysis unavailable", "ai_used": False}
