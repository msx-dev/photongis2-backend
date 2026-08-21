from collections.abc import Iterator
from typing import Any
import uuid

from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.runnables import RunnableConfig

from llm.agent import agent, checkpointer
from llm.context import AgentContext
from llm.conversation import ConversationManager

#Internal custom conversation manager
conversation_manager = ConversationManager(
    checkpointer=checkpointer,
)


def _extract_text_content(content: Any) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []

        for block in content:
            if isinstance(block, str):
                parts.append(block)
                continue

            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text")
                if isinstance(text, str):
                    parts.append(text)

        return "".join(parts)

    return ""

def chat_stream(
    user_message: str,
    user: Any,
    db: Any,
    project_id: uuid.UUID,
) -> Iterator[str]:
    """
    Run the LangGraph agent and stream the assistant response.

    Conversation history is stored by LangGraph's checkpointer.

    Runtime dependencies such as the authenticated user and database session
    are passed through AgentContext.
    """

    # ------------------------------------------------------------------------
    # 1. PREPARE CONVERSATION
    # ------------------------------------------------------------------------

    thread_id = conversation_manager.prepare(
        user_id=str(user.id),
        project_id=str(project_id),
    )

    # ------------------------------------------------------------------------
    # 2. LANGGRAPH CONFIGURATION
    # ------------------------------------------------------------------------

    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    # ------------------------------------------------------------------------
    # 3. REQUEST CONTEXT
    # ------------------------------------------------------------------------

    context = AgentContext(
        user=user,
        db=db,
        project_id=project_id,
    )

    # ------------------------------------------------------------------------
    # 4. STREAM LANGGRAPH
    # ------------------------------------------------------------------------

    for chunk, metadata in agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
                }
            ]
        },
        config=config,
        context=context,
        stream_mode="messages",
    ):

        # --------------------------------------------------------------------
        # 5. ONLY PROCESS LANGCHAIN MESSAGES
        # --------------------------------------------------------------------

        if not isinstance(chunk, BaseMessage):
            continue

        if isinstance(chunk, ToolMessage):
            continue

        if not isinstance(chunk, (AIMessage, AIMessageChunk)):
            continue

        content = _extract_text_content(chunk.content)

        if content:
            yield content

    # ------------------------------------------------------------------------
    # 8. RECORD SUCCESSFUL MESSAGE
    # ------------------------------------------------------------------------

    conversation_manager.record_message(
        user_id=str(user.id),
        project_id=str(project_id),
    )


# ============================================================================
# GET CURRENT THREAD ID
# ============================================================================

def get_current_thread_id(
    user: Any,
    project_id: uuid.UUID,
) -> str:
    """
    Return the authenticated user's current conversation thread ID.
    """

    return conversation_manager.current_thread_id(
        user_id=str(user.id),
        project_id=str(project_id),
    )


# ============================================================================
# GET CONVERSATION STATE
# ============================================================================


def get_conversation_messages(
    thread_id: str,
) -> list[BaseMessage]:
    """
    Get the messages stored in the LangGraph checkpoint
    for the given conversation.
    """

    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    checkpoint = checkpointer.get(config)

    if checkpoint is None:
        return []

    return checkpoint["channel_values"].get(
        "messages",
        [],
    )


def get_conversation_messages_for_display(
    thread_id: str,
) -> list[dict[str, str]]:
    """
    Return only user-visible chat messages.

    Tool messages and empty assistant tool-call messages are excluded.
    """

    display: list[dict[str, str]] = []

    for message in get_conversation_messages(thread_id):
        if isinstance(message, HumanMessage):
            content = _extract_text_content(message.content)
            if content.strip():
                display.append({"type": "human", "content": content})
            continue

        if isinstance(message, AIMessage):
            content = _extract_text_content(message.content)
            if content.strip():
                display.append({"type": "ai", "content": content})

    return display
