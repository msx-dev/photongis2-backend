from fastapi import APIRouter, Depends, status
from models import User
from sqlalchemy.orm import Session
from services import get_current_user
from database import get_db
from schemas import ProjectRooftop, RooftopUpdate
import uuid
from services import update_project_rooftop, delete_project_rooftop


rooftops_router = APIRouter(prefix="/rooftops", tags=["Rooftops"])


@rooftops_router.patch(
    "/{rooftop_id}", response_model=ProjectRooftop, status_code=status.HTTP_200_OK
)
def update_rooftop(
    rooftop_id: uuid.UUID,
    rooftop: RooftopUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_project_rooftop(rooftop_id, rooftop, db)


@rooftops_router.delete(
    "/{rooftop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rooftop(
    rooftop_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_project_rooftop(rooftop_id, db)
