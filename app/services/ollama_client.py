import httpx
from app.core.config import get_settings

_settings = get_settings()

async def ollama_health() -> bool:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # simple ping: list models
            r = await client.get(f"{_settings.OLLAMA_BASE_URL}/api/tags")
            return r.status_code == 200
    except Exception:
        return False


async def generate(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            f"{_settings.OLLAMA_BASE_URL}/api/generate",
            json={"model": _settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
        )
        r.raise_for_status()
        return r.json().get("response", "")