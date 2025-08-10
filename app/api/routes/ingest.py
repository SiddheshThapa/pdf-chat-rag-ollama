from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf_parser import extract_text_from_pdf_bytes
from app.services.chunker import text_to_chunks
from app.services.embeddings import embed_texts  # (kept in case you add FAISS later)
from app.services.retriever import get_collection, add_texts
from app.core.config import get_settings
import uuid

router = APIRouter(prefix="/ingest", tags=["ingest"])
_settings = get_settings()

@router.post("", response_model=dict)
async def ingest_pdf(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Upload a PDF")
    data = await file.read()
    text = extract_text_from_pdf_bytes(data)
    chunks = text_to_chunks(text, _settings.CHUNK_SIZE, _settings.CHUNK_OVERLAP)
    if not chunks:
        raise HTTPException(status_code=400, detail="No text extracted from PDF")

    # For Chroma, we can add documents directly; embeddings are computed internally if using 'embedding_function'.
    # To keep it simple here, we store raw chunks and rely on Chroma's default embedding (will fall back).
    # (Advanced: pass a custom embedding function that calls SentenceTransformer.)

    doc_id = str(uuid.uuid4())
    coll = get_collection("pdf_docs")
    add_texts(coll, chunks, doc_id)

    return {"doc_id": doc_id, "chunks": len(chunks)}
