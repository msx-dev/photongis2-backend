from langchain.tools import ToolRuntime, tool

from llm.context import AgentContext

from services import get_user_inverters


def _format_inverters_as_text(inverters) -> str:
    if not inverters:
        return "The user has no inverters saved yet."

    lines = [f"The user has {len(inverters)} inverter(s):"]

    for index, inverter in enumerate(inverters, start=1):
        lines.append(
            f"{index}. {inverter.name} — "
            f"max AC power {inverter.max_ac_power} W, "
            f"max DC power {inverter.max_dc_power} W, "
            f"efficiency {inverter.efficiency}%."
        )

    return "\n".join(lines)


@tool
def get_my_inverters(
    runtime: ToolRuntime[AgentContext],
) -> str:
    """
    Get all solar inverters belonging to the current authenticated user.
    """

    user = runtime.context.user
    db = runtime.context.db

    inverters = get_user_inverters(
        user=user,
        db=db,
    )

    return _format_inverters_as_text(inverters)
