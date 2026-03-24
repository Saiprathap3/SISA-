import asyncio
import json
import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.utils.logger import logger

# Section 2 Layer 4 Prompt Template
PROMPT_TEMPLATE = """
You are a cybersecurity analyst. Analyze these suspicious log entries:

{flagged_lines}

For each entry identify:
1. Attack type (brute_force/sql_injection/path_traversal/privilege_escalation/credential_leak/anomaly/other)
2. Severity: CRITICAL/HIGH/MEDIUM/LOW
3. Affected asset
4. Recommended action

Respond ONLY in this JSON format:
{{
  "findings": [
    {{
      "line": <number>,
      "attack_type": "",
      "severity": "",
      "asset": "",
      "action": ""
    }}
  ],
  "summary": "",
  "overall_risk": "CRITICAL|HIGH|MEDIUM|LOW"
}}
"""

class ClaudeGateway:
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.model = settings.CLAUDE_MODEL
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.version = "2023-06-01"

    async def analyze_suspicious_lines(self, flagged_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Call upgraded Claude Messages API with specific flagged lines (max 50)."""
        if not self.api_key:
            return {"findings": [], "summary": "AI Key missing", "overall_risk": "LOW"}
            
        # Limit to 50 lines
        flagged_entries = flagged_entries[:50]
        flagged_lines_str = "\n".join([f"Line {e['line_no']}: {e['content']}" for e in flagged_entries])
        
        prompt = PROMPT_TEMPLATE.format(flagged_lines=flagged_lines_str)
        
        # Section 5: Retry logic and timeout
        tries = 0
        while tries < 2:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(
                        self.api_url,
                        headers={
                            "x-api-key": self.api_key,
                            "anthropic-version": self.version,
                            "content-type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "max_tokens": 1024,
                            "messages": [{"role": "user", "content": prompt}]
                        }
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    
                    # Extract content
                    content = data["content"][0]["text"]
                    # Parse JSON safely
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        # Sometimes LLM outputs extra text, attempt to find JSON block
                        if "{" in content and "}" in content:
                            start = content.find("{")
                            end = content.rfind("}") + 1
                            return json.loads(content[start:end])
                        raise
                        
            except Exception as e:
                tries += 1
                if tries < 2:
                    await asyncio.sleep(1) # retry after 1s
                else:
                    logger.error(f"AI Analysis failed after retries: {str(e)}")
                    return {"findings": [], "summary": "AI Analysis unavailable", "overall_risk": "LOW"}
                    
        return {"findings": [], "summary": "AI Analysis unavailable", "overall_risk": "LOW"}
