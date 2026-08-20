from sqlalchemy.orm import Session
from models import User

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from llm.provider import model
from llm.prompts import SYSTEM_PROMPT
from llm.tools.inverter_tools import create_inverter_tools
from langchain_core.runnables import RunnableConfig

from langgraph.checkpoint.memory import InMemorySaver


# ---------------------------------------------------------------------------
# IN-MEMORY CHECKPOINTER
# ---------------------------------------------------------------------------
#
# This object stores the state of our LangGraph agents in server RAM.
#
# The important thing is that we create it ONCE when this module is loaded.
#
# We do NOT create it inside chat().
#
# If we created it inside chat(), the memory would be destroyed after
# every request, which would defeat the whole purpose.
#
# Because this object lives at module level, all requests handled by this
# Python process can access the same stored conversation state.
#
# IMPORTANT:
# This memory disappears when the Python process/server restarts.
#
# That's exactly what we currently want.
# ---------------------------------------------------------------------------

checkpointer = InMemorySaver()


# ---------------------------------------------------------------------------
# CHAT
# ---------------------------------------------------------------------------
#
# This is the function your FastAPI endpoint already calls:
#
#     reply = chat(message, current_user, db)
#
# We are keeping that interface unchanged.
# ---------------------------------------------------------------------------

def chat(
    user_message: str,
    user: User,
    db: Session,
) -> str:

    # -----------------------------------------------------------------------
    # Create tools for THIS authenticated user.
    #
    # This is important for security.
    #
    # We don't want the AI to have a generic "get all inverters" tool.
    # We want tools that operate using the current authenticated user.
    # -----------------------------------------------------------------------

    tools = create_inverter_tools(
        user=user,
        db=db,
    )

    # -----------------------------------------------------------------------
    # Create the LangChain/LangGraph agent.
    #
    # The checkpointer gives this agent persistent state between invocations.
    #
    # The state is identified using a "thread_id", which we provide below
    # when calling the agent.
    # -----------------------------------------------------------------------

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    # -----------------------------------------------------------------------
    # Identify this user's conversation.
    #
    # You said:
    #
    #   "One conversation per user."
    #
    # Therefore we can derive the thread ID from the authenticated user.
    #
    # User 42 -> "user:42"
    # User 87 -> "user:87"
    #
    # The frontend does NOT need to provide this ID.
    # -----------------------------------------------------------------------

    thread_id = f"user:{user.id}"

    # -----------------------------------------------------------------------
    # LangGraph needs the thread ID inside "configurable".
    #
    # This tells the checkpointer:
    #
    #   "Load the state belonging to this conversation."
    #
    # If this is the first message:
    #
    #   no previous state exists -> start fresh.
    #
    # If this is a later message:
    #
    #   load the previous state -> continue the conversation.
    # -----------------------------------------------------------------------

    config: RunnableConfig = {
    "configurable": {
        "thread_id": thread_id,
    }
}

    # -----------------------------------------------------------------------
    # Invoke the agent.
    #
    # We give it the NEW user message.
    #
    # LangGraph will combine this with the state it previously saved for
    # this thread.
    # -----------------------------------------------------------------------

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=user_message)
            ]
        },
        config=config,
    )

    # -----------------------------------------------------------------------
    # The agent returns its current state.
    #
    # "messages" contains the conversation messages, including any tool
    # calls/results that happened during the agent execution.
    #
    # The final message should be the assistant's response.
    # -----------------------------------------------------------------------

    messages = result["messages"]

    final_message = messages[-1]

    # -----------------------------------------------------------------------
    # Return the text back to FastAPI.
    # -----------------------------------------------------------------------

    return final_message.content