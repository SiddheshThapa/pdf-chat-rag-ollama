# app/main.py
from fastapi import FastAPI

from app.core.logging import setup_logging
from app.api.routes import health as health_route
from app.api.routes import ingest as ingest_route
from app.api.routes import ask as ask_route        # ← enable in Phase 3
from app.api.routes import metrics as metrics_route # ← enable in Phase 4

log = setup_logging()
app = FastAPI(title="Self-Healing RAG")

# Routers
app.include_router(health_route.router)
app.include_router(ingest_route.router)
app.include_router(ask_route.router)        # ← Phase 3
app.include_router(metrics_route.router)    # ← Phase 4

@app.get("/")
def root():
    return {"message": "Self-Healing RAG up. See /docs"}
