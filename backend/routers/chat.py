"""
JanSetu Mitra Sidebar Chatbot Routes
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.agents.chatbot import handle_chat_message
from backend.db import get_chat_history

router = APIRouter(prefix="/api/chat", tags=["JanSetu Mitra Chatbot"])


class ChatMessageRequest(BaseModel):
    session_id: str = Field(..., description="Unique browser or conversation session ID")
    message: str = Field(..., min_length=1, description="Citizen's question")
    user_id: Optional[int] = None
    language: Optional[str] = "en"


@router.post("")
@router.post("/message")
def send_chat_message(req: ChatMessageRequest):
    """Answers citizen questions regarding government schemes, eligibility, and documents."""
    result = handle_chat_message(
        session_id=req.session_id,
        message=req.message,
        user_id=req.user_id,
        language=req.language or "en"
    )
    # Ensure both 'reply' and 'response' keys exist for frontend compatibility
    reply_text = result.get("reply", "")
    result["response"] = reply_text
    return result


@router.get("/history/{session_id}")
def get_session_history(session_id: str, limit: int = 50):
    """Retrieves chat message history for a given session."""
    history = get_chat_history(session_id, limit=limit)
    return {"session_id": session_id, "messages": history}
