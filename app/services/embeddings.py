from sentence_transformers import SentenceTransformer
from functools import lru_cache
from app.core.config import get_settings

_settings = get_settings()

@lru_cache
def _model():
    return SentenceTransformer(_settings.EMBED_MODEL)

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = _model()
    return model.encode(texts, convert_to_numpy=False).tolist()
