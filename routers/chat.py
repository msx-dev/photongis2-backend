from fastapi import APIRouter, Depends
from models import User
from llm.orchestrator import chat
from services.auth import get_current_user
from sqlalchemy.orm import Session
from database import get_db

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chat_router.post("")
def ask_ai(
    message: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    reply = chat(
        message,
        current_user,
        db
    )

    return {
        "reply": reply
    }