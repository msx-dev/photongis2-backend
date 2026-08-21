from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from llm.context import AgentContext
from llm.provider import model
from llm.prompts import SYSTEM_PROMPT
from llm.tools.inverter_tools import get_my_inverters
from llm.tools.panel_tools import get_my_panels
from llm.tools.rooftop_tools import get_current_project_rooftops
from llm.tools.manual_tools import search_user_manual

checkpointer = InMemorySaver()

tools = [
    get_my_inverters,
    get_my_panels,
    get_current_project_rooftops,
    search_user_manual,
]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
    context_schema=AgentContext,
)
