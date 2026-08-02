from services import get_user_inverters

def get_my_inverters(user, db):
    inverters = get_user_inverters(
        user=user,
        db=db
    )

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