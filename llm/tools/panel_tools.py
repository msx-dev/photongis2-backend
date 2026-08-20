from langchain.tools import ToolRuntime, tool

from llm.context import AgentContext

from services import get_user_panels


def _format_panels_as_text(panels) -> str:
    if not panels:
        return "The user has no panel models saved yet."

    lines = [f"The user has {len(panels)} panel model(s):"]

    for index, panel in enumerate(panels, start=1):
        lines.append(
            f"{index}. {panel.name} — "
            f"{panel.width} mm x {panel.height} mm, "
            f"{panel.power} W per panel, "
            f"Vmp {panel.vmp} V, Voc {panel.voc} V, "
            f"Imp {panel.imp} A, Isc {panel.isc} A."
        )

    return "\n".join(lines)


@tool
def get_my_panels(
    runtime: ToolRuntime[AgentContext],
) -> str:
    """
    Get all solar panel models belonging to the current authenticated user.
    """

    panels = get_user_panels(
        user=runtime.context.user,
        db=runtime.context.db,
    )

    return _format_panels_as_text(panels)
