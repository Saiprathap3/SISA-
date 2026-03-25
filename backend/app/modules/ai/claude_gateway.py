import anthropic
import os
import json
import asyncio
import traceback
from typing import List, Dict
from datetime import datetime


def _get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    return anthropic.Anthropic(api_key=api_key)


def generate_fallback_insights(findings: List[Dict]) -> List[str]:
    """
    Rule-based insights when Claude API is unavailable.
    Always returns at least 1 meaningful insight.
    """
    insights = []
    types = {f.get("type", "") for f in findings}
    
    type_map = {
        "password": ("CRITICAL", "Password exposed in plain text — "
                     "change immediately and audit all access logs"),
        "api_key": ("HIGH", "API key exposed — rotate via provider "
                    "dashboard immediately"),
        "aws_key": ("CRITICAL", "AWS access key exposed — disable in "
                    "IAM console immediately and check CloudTrail"),
        "secret": ("CRITICAL", "Hardcoded secret detected — move to "
                   "environment variables and revoke exposed value"),
        "hardcoded_secret": ("CRITICAL", "Hardcoded auth secret — "
                             "rotate and use a secrets manager"),
        "bearer_token": ("HIGH", "Bearer token exposed — revoke and "
                         "reissue this token immediately"),
        "jwt_token": ("HIGH", "JWT token exposed — invalidate this "
                      "token and audit active sessions"),
        "token": ("HIGH", "Auth token exposed — revoke and reissue"),
        "brute_force": ("HIGH", "Brute force attack detected — "
                        "block the source IP and enable rate limiting"),
        "sql_injection": ("HIGH", "SQL injection patterns found — "
                          "use parameterized queries immediately"),
        "command_injection": ("HIGH", "Command injection patterns — "
                              "sanitize all inputs before processing"),
        "stack_trace": ("MEDIUM", "Stack trace reveals internals — "
                        "disable verbose error logging in production"),
        "debug_mode": ("MEDIUM", "Debug mode active in production — "
                       "disable immediately to prevent info disclosure"),
        "email": ("LOW", "Email addresses in logs — review data "
                  "retention policy and implement log sanitization"),
        "high_entropy_string": ("HIGH", "High-entropy string detected — "
                                "likely an exposed secret or encoded token"),
        "repeated_failures": ("HIGH", "Repeated auth failures — "
                              "possible brute force; enable account lockout"),
        "multi_pattern_line": ("CRITICAL", "Multiple risk patterns on "
                               "same line — high-confidence threat indicator"),
    }

    # Add finding-specific insight with line number
    for finding_type, (level, message) in type_map.items():
        if finding_type in types:
            matching = next(
                (f for f in findings if f.get("type") == finding_type), None
            )
            line_ref = (f" (line {matching['line']})" 
                       if matching and matching.get("line") else "")
            insights.append(f"{level}: {message}{line_ref}")
            if len(insights) >= 4:
                break

    if not insights:
        insights.append(
            "Review all detected findings and apply "
            "principle of least privilege"
        )

    return insights


async def get_ai_insights(
    findings: List[Dict],
    content_type: str,
    raw_content: str = ""
) -> List[str]:
    """
    Get AI-powered insights from Claude (claude-sonnet-4-6).
    Falls back to rule-based insights if Claude unavailable.
    This is the ONLY AI model used in this platform.
    """
    if not findings:
        return ["No sensitive data detected. Content appears secure."]

    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("AI SKIP: No API key — using fallback insights")
        return generate_fallback_insights(findings)

    raw = ""
    try:
        client = _get_client()

        # Build concise findings summary (max 10 to stay under token limit)
        summary = json.dumps([
            {
                "type": f.get("type"),
                "risk": f.get("risk"),
                "line": f.get("line"),
                "category": f.get("category")
            }
            for f in findings[:10]
        ], indent=2)

        prompt = f"""You are a cybersecurity expert. 
Analyze these security findings from {content_type} input:

{summary}

Provide exactly 3 specific, actionable security insights.
Each insight MUST:
- Reference the specific finding type and line number
- State the severity (CRITICAL/HIGH/MEDIUM/LOW)
- Give a concrete remediation action

Return ONLY a valid JSON array of exactly 3 strings.
Example: ["CRITICAL: Password at line 3 — rotate immediately", 
          "HIGH: API key at line 4 — revoke via provider dashboard",
          "MEDIUM: Stack trace at line 5 — disable verbose logging"]

Return ONLY the JSON array. No explanation. No markdown."""

        # Run blocking SDK call in thread pool (correct async pattern)
        loop = asyncio.get_event_loop()
        message = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
            ),
            timeout=25.0
        )

        raw = message.content[0].text.strip()
        print(f"CLAUDE OK: {raw[:120]}")

        # Clean markdown fences if present
        clean = raw
        for fence in ["```json", "```JSON", "```"]:
            clean = clean.replace(fence, "")
        clean = clean.strip()

        parsed = json.loads(clean)
        if isinstance(parsed, list) and len(parsed) > 0:
            print(f"AI SUCCESS: {len(parsed)} insights from claude-sonnet-4-6")
            return [str(i) for i in parsed[:5]]

        return generate_fallback_insights(findings)

    except asyncio.TimeoutError:
        print("AI TIMEOUT: Claude >25s — using fallback")
    except json.JSONDecodeError as e:
        print(f"AI JSON ERROR: {e}")
        if raw:
            # Salvage plain text lines
            lines = [
                l.strip().strip('"-•*[] ') 
                for l in raw.split('\n') 
                if len(l.strip()) > 20
            ]
            if lines:
                return lines[:3]
    except anthropic.AuthenticationError:
        print("AI AUTH ERROR: Invalid ANTHROPIC_API_KEY")
    except anthropic.RateLimitError:
        print("AI RATE LIMIT: Quota exceeded")
    except anthropic.APIConnectionError:
        print("AI CONNECTION ERROR: Cannot reach Anthropic API")
    except Exception as e:
        print(f"AI ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()

    return generate_fallback_insights(findings)
