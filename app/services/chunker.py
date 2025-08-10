def text_to_chunks(text: str, chunk_size: int, overlap: int):
    if not text:
        return []
    tokens = text.split()
    chunks, i = [], 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += max(1, chunk_size - overlap)
    return chunks
