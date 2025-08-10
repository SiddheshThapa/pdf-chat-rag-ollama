from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class IngestResponse(BaseModel):
    doc_id: str
    chunks: int

class AskResponse(BaseModel):
    answer: str
    sources: List[str] = []
    used_cache: bool = False
    metrics: Optional[Dict[str, Any]] = None   # ← NEW
    guardrail_passed: bool = True              # ← NEW

class MetricsResponse(BaseModel):
    latency_ms: float
    cache_hit_rate: float
    qps: Optional[float] = None
