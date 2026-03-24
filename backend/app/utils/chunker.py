from typing import List


def chunk_lines(lines: List[str], chunk_size: int = 500) -> List[List[str]]:
    """Split a list of strings into a list of chunks.

    Each chunk is a list of up to `chunk_size` items. Returns a list of chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    return [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
