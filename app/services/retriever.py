# app/services/retriever.py
import os
import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction  # NEW
from app.core.config import get_settings

_settings = get_settings()
_embed_fn = DefaultEmbeddingFunction()  # NEW

def ensure_vector_dir() -> str:
    os.makedirs(_settings.VECTOR_DIR, exist_ok=True)
    return os.path.abspath(_settings.VECTOR_DIR)

def _client():
    ensure_vector_dir()
    return chromadb.Client(ChromaSettings(persist_directory=_settings.VECTOR_DIR))

def get_collection(name: str = "pdf_docs"):
    client = _client()
    # pass embedding_function explicitly
    return client.get_or_create_collection(
        name=name,
        embedding_function=_embed_fn,
        metadata={"hnsw:space": "cosine"},
    )

def add_texts(collection, texts: list[str], doc_id: str):
    ids = [f"{doc_id}_{i}" for i in range(len(texts))]
    collection.add(ids=ids, documents=texts)

def query(collection, query_texts: list[str], k: int = 5):
    return collection.query(query_texts=query_texts, n_results=k)
