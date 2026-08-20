from collections.abc import Iterator
from typing import Any

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig

from llm.agent import agent, checkpointer
from llm.context import AgentContext
from llm.conversation import ConversationManager


# ============================================================================
# CONVERSATION MANAGER
# ============================================================================
#
# IMPORTANT:
# This uses the EXACT SAME checkpointer instance as the LangGraph agent.
#
# llm.agent:
#
#     checkpointer = InMemorySaver()
#
#     agent = create_agent(
#         ...,
#         checkpointer=checkpointer,
#     )
#
# Therefore ConversationManager can delete the same threads that the agent
# uses for its conversation state.
# ============================================================================

conversation_manager = ConversationManager(
    checkpointer=checkpointer,
)


# ============================================================================
# CHAT STREAM
# ============================================================================

def chat_stream(
    user_message: str,
    user: Any,
    db: Any,
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

        # --------------------------------------------------------------------
        # 6. EXTRACT CONTENT
        # --------------------------------------------------------------------

        content = chunk.content

        # --------------------------------------------------------------------
        # 7. YIELD TEXT
        # --------------------------------------------------------------------

        if isinstance(content, str) and content:
            yield content

    # ------------------------------------------------------------------------
    # 8. RECORD SUCCESSFUL MESSAGE
    # ------------------------------------------------------------------------

    conversation_manager.record_message(
        user_id=str(user.id),
    )


# ============================================================================
# GET CURRENT THREAD ID
# ============================================================================

def get_current_thread_id(
    user: Any,
) -> str:
    """
    Return the authenticated user's current conversation thread ID.
    """

    return conversation_manager.current_thread_id(
        user_id=str(user.id),
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