from langchain.tools import ToolRuntime, tool

from llm.context import AgentContext

from services import get_user_inverters


# ============================================================================
# GET MY INVERTERS
# ============================================================================
#
# This tool retrieves the inverters belonging to the CURRENT authenticated
# user.
#
# LangChain automatically provides ToolRuntime when this tool is executed.
#
# ToolRuntime[AgentContext] tells Pylance:
#
#     runtime.context -> AgentContext
#
# Therefore:
#
#     runtime.context.user
#     runtime.context.db
#
# are both correctly typed.
#
# The runtime parameter is NOT something the LLM supplies.
# LangChain injects it automatically.
# ============================================================================


@tool
def get_my_inverters(
    runtime: ToolRuntime[AgentContext],
) -> list[dict]:
    """
    Get all solar inverters belonging to the current authenticated user.
    """

    # ------------------------------------------------------------------------
    # Get request-specific context.
    # ------------------------------------------------------------------------

    user = runtime.context.user
    db = runtime.context.db


    # ------------------------------------------------------------------------
    # Use your existing application service.
    #
    # The service remains responsible for database access.
    # ------------------------------------------------------------------------

    inverters = get_user_inverters(
        user=user,
        db=db,
    )


    # ------------------------------------------------------------------------
    # Convert SQLAlchemy models into plain dictionaries.
    #
    # We should never send ORM objects directly to the LLM.
    # ------------------------------------------------------------------------

    return [
        {
            "id": str(inverter.id),
            "name": inverter.name,
            "max_ac_power": inverter.max_ac_power,
            "max_dc_power": inverter.max_dc_power,
            "efficiency": inverter.efficiency,
        }
        for inverter in inverters
    ]