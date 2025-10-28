from fastapi import APIRouter, Depends
from models import User
from sqlalchemy.orm import Session
from services import get_current_user
from database import get_db
from schemas import ProjectRooftop
import uuid
from services import get_projects_rooftops


rooftops_router = APIRouter(prefix="/rooftops", tags=["Rooftops"])


@rooftops_router.get("/{project_id}", response_model=list[ProjectRooftop])
def get_project_rooftops(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_projects_rooftops(project_id, db)
