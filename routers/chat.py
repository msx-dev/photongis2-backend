from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from database import get_db
from llm.orchestrator import (
    chat_stream,
    get_conversation_messages,
    get_current_thread_id,
)
from models import User
from services.auth import get_current_user


chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# =============================================================================
# STREAM CHAT
# =============================================================================

@chat_router.post("")
def ask_ai(
    message: str,
    current_user: User = Depends(
        get_current_user,
    ),
    db=Depends(get_db),
):
    """
    Send a message and stream the assistant response.
    """

    return StreamingResponse(
        chat_stream(
            user_message=message,
            user=current_user,
            db=db,
        ),
        media_type="text/plain",
    )


# =============================================================================
# GET CURRENT CONVERSATION
# =============================================================================

@chat_router.get("/current")
def get_current_conversation(
    current_user: User = Depends(
        get_current_user,
    ),
):
    """
    Return the authenticated user's current conversation.
    """

    thread_id = get_current_thread_id(
        current_user,
    )

    messages = get_conversation_messages(
        thread_id,
    )

    return {
        "thread_id": thread_id,
        "messages": messages,
    }


# =============================================================================
# GET SPECIFIC CONVERSATION
# =============================================================================

@chat_router.get("/{thread_id}")
def get_conversation(
    thread_id: str,
    current_user: User = Depends(
        get_current_user,
    ),
):
    """
    Return a specific conversation.

    Currently, the user may only access their current conversation.
    """

    current_thread_id = get_current_thread_id(
        current_user,
    )

    # -------------------------------------------------------------------------
    # SECURITY
    # -------------------------------------------------------------------------

    if thread_id != current_thread_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this conversation.",
        )

    # -------------------------------------------------------------------------
    # GET MESSAGES
    # -------------------------------------------------------------------------

    messages = get_conversation_messages(
        thread_id,
    )

    # -------------------------------------------------------------------------
    # CHECK WHETHER CONVERSATION EXISTS
    # -------------------------------------------------------------------------

    if not messages:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return {
        "thread_id": thread_id,
        "messages": messages,
    }