# app/schemas/request.py
from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str
    top_k: int = 5