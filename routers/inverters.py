import uuid
from fastapi import APIRouter, Depends, status
from database import get_db
from services.auth import get_current_user
from sqlalchemy.orm import Session
from schemas import UserInverter, InverterCreate
from models import User
from services import get_user_inverters, create_new_user_inverter, delete_user_inverter


inverters_router = APIRouter(prefix="/inverters", tags=["Inverters"])


@inverters_router.get("", response_model=list[UserInverter])
def get_all_user_inverters(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_user_inverters(current_user, db)


@inverters_router.post("", response_model=UserInverter, status_code=status.HTTP_201_CREATED)
def create_new_inverter(
    inverter: InverterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_user_inverter(inverter, db, current_user)


@inverters_router.delete("/{inverter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inverter(
    inverter_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_user_inverter(inverter_id, db, current_user)
