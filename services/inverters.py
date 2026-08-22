import uuid
from fastapi import HTTPException, status, responses
from models import User, Inverter
from sqlalchemy.orm import Session
from schemas import InverterCreate, UserInverter


def get_user_inverters(user: User, db: Session) -> list[Inverter]:
    return (
        db.query(Inverter)
        .filter(Inverter.owner_id == user.id)
        .order_by(Inverter.created_at.asc())
        .all()
    )


def create_new_user_inverter(
    inverter: InverterCreate, db: Session, current_user: User
) -> UserInverter:

    db_inverter = Inverter(
        name=inverter.name,
        max_ac_power=inverter.max_ac_power,
        max_dc_power=inverter.max_dc_power,
        max_dc_voltage=inverter.max_dc_voltage,
        mppt_min_voltage=inverter.mppt_min_voltage,
        mppt_max_voltage=inverter.mppt_max_voltage,
        start_voltage=inverter.start_voltage or 100,
        max_current_per_mppt=inverter.max_current_per_mppt or 15.0,
        mppt_count=inverter.mppt_count or 1,
        max_strings_per_mppt=inverter.max_strings_per_mppt or 1,
        efficiency=inverter.efficiency or 0.97,
        owner_id=current_user.id,
    )

    db.add(db_inverter)
    db.commit()
    db.refresh(db_inverter)

    return db_inverter


def delete_user_inverter(inverter_id: uuid.UUID, db: Session, current_user: User):
    inverter = (
        db.query(Inverter)
        .filter(Inverter.id == inverter_id, Inverter.owner_id == current_user.id)
        .first()
    )

    if not inverter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inverter with id {inverter_id} not found.",
        )

    db.delete(inverter)
    db.commit()

    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)