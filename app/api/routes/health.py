from fastapi import APIRouter
# from app.services.cache import ping_redis
from app.services.ollama_client import ollama_health
from app.services.retriever import ensure_vector_dir

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health():
    vector_dir = ensure_vector_dir()
    return {
        "status": "ok",
        # "redis": ping_redis(),
        "ollama": await ollama_health(),
        "vector_dir": vector_dir,
    }
