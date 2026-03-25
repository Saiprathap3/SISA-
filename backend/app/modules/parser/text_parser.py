from typing import Dict


def parse_text(content: str) -> Dict:
    """Return content and simple metadata: char_count, word_count, line_count."""
    if content is None:
        content = ""
    char_count = len(content)
    word_count = len(content.split())
    line_count = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
    return {"content": content, "metadata": {"char_count": char_count, "word_count": word_count, "line_count": line_count}}
