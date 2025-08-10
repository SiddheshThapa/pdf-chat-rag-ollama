import time
from collections import deque

_requests = 0
_errors = 0
_latencies_ms = deque(maxlen=200)  # moving window

def record_request():
    global _requests
    _requests += 1

def record_error():
    global _errors
    _errors += 1

def record_latency_ms(ms: float):
    _latencies_ms.append(ms)

def snapshot():
    avg = (sum(_latencies_ms) / len(_latencies_ms)) if _latencies_ms else 0.0
    return {"requests": _requests, "errors": _errors, "avg_latency_ms": avg}
