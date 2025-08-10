import re

# Simple PII regexes (good enough for demos)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){2}\d{4}")

def contains_pii(text: str) -> bool:
    if not text:
        return False
    return bool(EMAIL_RE.search(text) or PHONE_RE.search(text))

def context_is_confident(contexts: list[str], min_chunks: int = 1, min_chars: int = 50) -> bool:
    """Reject if too little context (reduces hallucinations)."""
    ctx = [c for c in contexts if c]
    if len(ctx) < min_chunks:
        return False
    return sum(len(c) for c in ctx) >= min_chars
