from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str
    status: str = "success"
    user_id: Optional[str] = None
    session_id: Optional[str] = None 