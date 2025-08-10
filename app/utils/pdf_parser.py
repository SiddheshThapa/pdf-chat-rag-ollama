from pypdf import PdfReader

def extract_text_from_pdf_bytes(data: bytes) -> str:
    reader = PdfReader(io := __import__("io").BytesIO(data))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            pass
    return "\n".join(texts).strip()
