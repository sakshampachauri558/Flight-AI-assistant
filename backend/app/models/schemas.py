from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    booking_reference: str

class ChatResponse(BaseModel):
    response: str
    escalated: bool = False
    actions_taken: List[str] = []
    policies_applied: List[str] = []
