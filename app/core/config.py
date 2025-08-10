# app/core/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict  # <-- changed import

class Settings(BaseSettings):
    EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 120

    VECTOR_DB: str = "chroma"
    VECTOR_DIR: str = "./data/indexes/chroma"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b"

    # Pydantic v2 way to set env file, replaces the old inner Config class
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
