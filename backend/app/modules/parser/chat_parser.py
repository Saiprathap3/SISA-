from typing import List, Dict, Any
import json


def parse_chat(messages: List[Dict[str, Any]] | str) -> str:
    """Normalize chat messages into a single string.

    If messages is a list, format as 'ROLE: content\n'. If str, try parse JSON into list.
    """
    if isinstance(messages, list):
        return "\n".join(f"{m.get('role','user').upper()}: {m.get('content','')}" for m in messages)
    if isinstance(messages, str):
        try:
            parsed = json.loads(messages)
            if isinstance(parsed, list):
                return parse_chat(parsed)
        except Exception:
            pass
        return messages
    return ""
