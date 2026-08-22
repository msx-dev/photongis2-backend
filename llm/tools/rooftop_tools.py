from langchain.tools import ToolRuntime, tool

from llm.context import AgentContext

from services import get_projects_rooftops, get_user_project_by_id


def _count_placed_panels(additional_panels) -> int:
    # The first panel a user places is stored as `initial_polygon`, not in
    # `additional_panels` (which only holds the auto-filled panels around it).
    initial_panel_count = 1

    if isinstance(additional_panels, dict):
        return len(additional_panels) + initial_panel_count

    return initial_panel_count


def _format_production(solar_production) -> str:
    if not solar_production:
        return "Production estimate is not available yet."

    yearly = solar_production.get("yearly") if isinstance(solar_production, dict) else None

    if not yearly:
        return "Production estimate is not available yet."

    yearly_kwh = yearly.get("E_y")
    monthly_kwh = yearly.get("E_m")
    daily_kwh = yearly.get("E_d")

    parts: list[str] = []

    if yearly_kwh is not None:
        parts.append(f"estimated yearly production {yearly_kwh} kWh")

    if monthly_kwh is not None:
        parts.append(f"average monthly production {monthly_kwh} kWh")

    if daily_kwh is not None:
        parts.append(f"average daily production {daily_kwh} kWh")

    if not parts:
        return "Production estimate is not available yet."

    return ", ".join(parts).capitalize() + "."


def _format_rooftops_as_text(rooftops) -> str:
    if not rooftops:
        return "This project has no rooftops yet."

    lines = [f"This project has {len(rooftops)} rooftop group(s):"]

    for index, rooftop in enumerate(rooftops, start=1):
        panel_count = _count_placed_panels(rooftop.get("additional_panels"))
        panel_name = rooftop.get("name") or "Unknown panel"
        panel_power = rooftop.get("power")
        total_installed_power = (
            panel_count * panel_power
            if panel_count and panel_power is not None
            else None
        )

        lines.append(
            f"{index}. Rooftop group {index} uses {panel_name} "
            f"({rooftop.get('width')} mm x {rooftop.get('height')} mm, "
            f"{panel_power} W per panel)."
        )
        lines.append(
            f"   Orientation: {rooftop.get('angle')}° azimuth, "
            f"{rooftop.get('slope')}° slope, "
            f"{rooftop.get('spacing')} mm spacing."
        )
        lines.append(
            f"   Panels placed on this roof: {panel_count}."
        )

        if total_installed_power is not None:
            lines.append(
                f"   Total installed DC power on this roof: {total_installed_power} W."
            )

        lines.append(f"   {_format_production(rooftop.get('solar_production'))}")

    return "\n".join(lines)


@tool
def get_current_project_rooftops(
    runtime: ToolRuntime[AgentContext],
) -> str:
    """
    Get all rooftops in the user's current project, including panel layout,
    panel specifications, and solar production estimates.

    Rooftop and panel data can change between messages (the user may edit
    the layout in the app), so always call this tool again to get fresh
    data instead of reusing a previous result from this conversation.
    """

    user = runtime.context.user
    db = runtime.context.db
    project_id = runtime.context.project_id

    get_user_project_by_id(
        project_id=project_id,
        user=user,
        db=db,
    )

    rooftops = get_projects_rooftops(
        project_id=project_id,
        db=db,
    )

    return _format_rooftops_as_text(rooftops)
