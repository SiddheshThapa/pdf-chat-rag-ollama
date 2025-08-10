from fastapi import APIRouter
from app.services.metrics import snapshot

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("")
def metrics():
    return snapshot()
