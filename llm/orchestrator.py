from sqlalchemy.orm import Session

from models import User

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from llm.agent import agent, checkpointer
from llm.context import AgentContext
from llm.conversation import ConversationManager


# =============================================================================
# CONVERSATION MANAGER
# =============================================================================
#
# ONE manager exists for the lifetime of this Python process.
#
# It manages:
#
#     - 100-message limit
#     - 30-minute inactivity timeout
#     - deleting expired LangGraph threads
#     - creating new conversation generations
#
# It uses the SAME checkpointer as the agent.
# =============================================================================


conversation_manager = ConversationManager(
    checkpointer=checkpointer,
)


# =============================================================================
# CHAT
# =============================================================================


def chat(
    user_message: str,
    user: User,
    db: Session,
) -> str:

    # =========================================================================
    # 1. IDENTIFY USER
    # =========================================================================

    user_id = str(user.id)


    # =========================================================================
    # 2. PREPARE CONVERSATION
    # =========================================================================
    #
    # This checks:
    #
    #     - Have we reached 100 messages?
    #     - Has the conversation been inactive for 30 minutes?
    #
    # If expired:
    #
    #     OLD THREAD
    #          ↓
    #     DELETE FROM CHECKPOINTER
    #          ↓
    #     NEW GENERATION
    #
    # Otherwise we continue the existing thread.
    # =========================================================================

    thread_id = conversation_manager.prepare(
        user_id=user_id,
    )


    # =========================================================================
    # 3. LANGGRAPH CONFIG
    # =========================================================================
    #
    # thread_id tells LangGraph which conversation state belongs to this user.
    # =========================================================================

    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
        }
    }


    # =========================================================================
    # 4. REQUEST CONTEXT
    # =========================================================================
    #
    # This is request-specific information.
    #
    # Tools can access:
    #
    #     runtime.context.user
    #     runtime.context.db
    # =========================================================================

    context = AgentContext(
        user=user,
        db=db,
    )


    # =========================================================================
    # 5. RUN AGENT
    # =========================================================================
    #
    # LangGraph handles the complete agent loop:
    #
    #     user message
    #          ↓
    #        model
    #          ↓
    #     tool required?
    #       /       \
    #     yes        no
    #      ↓          ↓
    #    tool       answer
    #      ↓
    #    model
    #      ↓
    #    answer
    #
    # The resulting state is automatically saved by InMemorySaver.
    # =========================================================================

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=user_message,
                )
            ]
        },
        config=config,
        context=context,
    )


    # =========================================================================
    # 6. RECORD SUCCESSFUL USER MESSAGE
    # =========================================================================
    #
    # Only record the message AFTER the agent successfully finished.
    # =========================================================================

    conversation_manager.record_message(
        user_id=user_id,
    )


    # =========================================================================
    # 7. GET FINAL MESSAGE
    # =========================================================================

    final_message = result["messages"][-1]


    # =========================================================================
    # 8. RETURN TO FASTAPI
    # =========================================================================

    return final_message.content