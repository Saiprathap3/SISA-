from typing import Dict, Any

try:
    from pypdf import PdfReader  # type: ignore
except Exception:
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception:
        PdfReader = None  # type: ignore

try:
    from docx import Document  # type: ignore
except Exception:
    Document = None  # type: ignore


MAX_SIZE_BYTES = 10 * 1024 * 1024


async def parse_file(filename: str, content: bytes) -> Dict[str, Any]:
    """Parse file bytes into text content and metadata.

    Supports PDF, DOCX, TXT. Validates size.
    """
    size = len(content)
    if size > MAX_SIZE_BYTES:
        raise ValueError("File exceeds maximum allowed size")

    lower = filename.lower()
    import io

    if lower.endswith(".pdf"):
        if PdfReader:
            try:
                reader = PdfReader(io.BytesIO(content))
                pages = [p.extract_text() or "" for p in getattr(reader, "pages", [])]
                text = "\n".join(pages)
                metadata = {"pages": len(pages), "file_type": "pdf", "size_bytes": size}
                return {"content": text, "metadata": metadata}
            except Exception:
                # fallback to raw bytes decode if PDF parsing fails
                try:
                    text = content.decode("utf-8", errors="replace")
                except Exception:
                    text = ""
                metadata = {"pages": None, "file_type": "pdf_unparsed", "size_bytes": size}
                return {"content": text, "metadata": metadata}
        else:
            # PDF library not available; return best-effort decoded text
            try:
                text = content.decode("utf-8", errors="replace")
            except Exception:
                text = ""
            metadata = {"pages": None, "file_type": "pdf_unparsed", "size_bytes": size}
            return {"content": text, "metadata": metadata}

    if lower.endswith(".docx") or lower.endswith(".doc"):
        if Document:
            try:
                doc = Document(io.BytesIO(content))
                paragraphs = [p.text for p in doc.paragraphs]
                text = "\n".join(paragraphs)
                metadata = {"pages": None, "file_type": "docx", "size_bytes": size}
                return {"content": text, "metadata": metadata}
            except Exception:
                pass
        # fallback
        try:
            text = content.decode("utf-8", errors="replace")
        except Exception:
            text = ""
        metadata = {"pages": None, "file_type": "docx_unparsed", "size_bytes": size}
        return {"content": text, "metadata": metadata}

    # fallback to text, attempt to use chardet if available
    try:
        import chardet

        detected = chardet.detect(content)
        encoding = detected.get("encoding") or "utf-8"
    except Exception:
        encoding = "utf-8"
    text = content.decode(encoding, errors="replace")
    metadata = {"pages": None, "file_type": "txt", "size_bytes": size, "encoding": encoding}
    return {"content": text, "metadata": metadata}
