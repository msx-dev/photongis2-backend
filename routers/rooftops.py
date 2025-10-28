from fastapi import APIRouter, Depends, status
from models import User
from sqlalchemy.orm import Session
from services import get_current_user
from database import get_db
from schemas import ProjectRooftop, RooftopCreate, RooftopUpdate
import uuid
from services import get_projects_rooftops, create_new_rooftop


rooftops_router = APIRouter(prefix="/rooftops", tags=["Rooftops"])


@rooftops_router.get("/{project_id}", response_model=list[ProjectRooftop])
def get_project_rooftops(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_projects_rooftops(project_id, db)


@rooftops_router.post(
    "/{project_id}", response_model=ProjectRooftop, status_code=status.HTTP_201_CREATED
)
def create_project_rooftop(
    project_id: uuid.UUID,
    rooftop: RooftopCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_rooftop(rooftop, project_id, db)


@rooftops_router.patch(
    "/{project_id}", response_model=ProjectRooftop, status_code=status.HTTP_200_OK
)
def update_project_rooftop(
    project_id: uuid.UUID,
    rooftop: RooftopUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_project_rooftop(project_id, rooftop, current_user)
