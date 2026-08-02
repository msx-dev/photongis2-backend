from fastapi import APIRouter

from llm.orchestrator import chat

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chat_router.post("")
def ask_ai(message: str):

    reply = chat(message)

    return {
        "reply": reply
    }