from fastapi import APIRouter, HTTPException
from app.schemas.request import AskRequest
from app.schemas.response import AskResponse
from app.services.retriever import get_collection, query
from app.services.ollama_client import generate
from app.core.guards import contains_pii, context_is_confident
from app.services.metrics import record_request, record_error, record_latency_ms, snapshot
import time

router = APIRouter(prefix="/ask", tags=["ask"])

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer ONLY from the provided context. "
    "If the answer isn't in the context, say you don't know."
)

def build_prompt(q: str, contexts: list[str]) -> str:
    context_block = "\n\n".join([f"- {c}" for c in contexts])
    return f"{SYSTEM_PROMPT}\n\nContext:\n{context_block}\n\nQuestion: {q}\nAnswer:"

@router.post("", response_model=AskResponse)
async def ask(req: AskRequest):
    record_request()
    q = req.query.strip()

    # Guardrails
    if contains_pii(q):
        record_error()
        raise HTTPException(status_code=403, detail="Query contains PII. Please remove emails/phone numbers.")

    t0 = time.time()

    # Retrieve
    coll = get_collection("pdf_docs")
    results = query(coll, [q], k=req.top_k)
    contexts = results.get("documents", [[]])[0]
    ids = results.get("ids", [[]])[0]

    if not context_is_confident(contexts, min_chunks=1, min_chars=50):
        record_error()
        raise HTTPException(status_code=422, detail="Not enough reliable context. Try a more specific question.")

    # Generate
    prompt = build_prompt(q, contexts)
    answer = await generate(prompt)

    # Metrics
    record_latency_ms((time.time() - t0) * 1000.0)

    return AskResponse(
        answer=answer,
        sources=ids,
        used_cache=False,
        metrics=snapshot(),
        guardrail_passed=True,
    )
