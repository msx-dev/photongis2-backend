from services import get_user_inverters

from langchain_core.tools import tool


def create_inverter_tools(user, db):
    """
    Create the LangChain tools that are available for this request.

    `user` and `db` come from our FastAPI application.
    They are NOT arguments that the LLM gets to choose.

    This is important because we don't want the LLM
    to provide things like user IDs or database sessions.
    """

    @tool
    def get_my_inverters() -> list[dict]:
        """
        Get all inverters belonging to the current user.

        Use this tool whenever the user asks about their
        inverters or needs information about their inverters.
        """

        # Get the current user's inverters from our database.
        inverters = get_user_inverters(
            user=user,
            db=db,
        )

        # Convert SQLAlchemy objects into plain dictionaries
        # that can safely be returned to the LLM.
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

    # Return the tools available to this particular request.
    return [
        get_my_inverters,
    ]