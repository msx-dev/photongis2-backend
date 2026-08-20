from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from llm.context import AgentContext
from llm.provider import model
from llm.prompts import SYSTEM_PROMPT
from llm.tools.inverter_tools import get_my_inverters


# =============================================================================
# CHECKPOINTER
# =============================================================================
#
# InMemorySaver stores LangGraph conversation state in server memory.
#
# It lives as long as this Python process lives.
#
# We also expose this object so ConversationManager can delete expired
# conversations using the public delete_thread() API.
# =============================================================================


checkpointer = InMemorySaver()


# =============================================================================
# TOOLS
# =============================================================================

tools = [
    get_my_inverters,
]


# =============================================================================
# AGENT
# =============================================================================

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
    context_schema=AgentContext,
)