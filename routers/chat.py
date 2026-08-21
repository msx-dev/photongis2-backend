import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from database import get_db
from llm.orchestrator import (
    chat_stream,
    get_conversation_messages_for_display,
    get_current_thread_id,
)
from models import User
from services.auth import get_current_user
from services import get_user_project_by_id


chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@chat_router.post("")
def ask_ai(
    message: str,
    project_id: uuid.UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db=Depends(get_db),
):
    """
    Send a message and stream the assistant response.
    """

    get_user_project_by_id(
        project_id=project_id,
        user=current_user,
        db=db,
    )

    return StreamingResponse(
        chat_stream(
            user_message=message,
            user=current_user,
            db=db,
            project_id=project_id,
        ),
        media_type="text/plain",
    )

@chat_router.get("/current")
def get_current_conversation(
    project_id: uuid.UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db=Depends(get_db),
):
    get_user_project_by_id(
        project_id=project_id,
        user=current_user,
        db=db,
    )

    thread_id = get_current_thread_id(
        current_user,
        project_id,
    )

    messages = get_conversation_messages_for_display(
        thread_id,
    )

    return {
        "thread_id": thread_id,
        "project_id": str(project_id),
        "messages": messages,
    }

@chat_router.get("/{thread_id}")
def get_conversation(
    thread_id: str,
    project_id: uuid.UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db=Depends(get_db),
):
    get_user_project_by_id(
        project_id=project_id,
        user=current_user,
        db=db,
    )

    current_thread_id = get_current_thread_id(
        current_user,
        project_id,
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

    messages = get_conversation_messages_for_display(
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
        "project_id": str(project_id),
        "messages": messages,
    }
