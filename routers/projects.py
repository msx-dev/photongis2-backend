from fastapi import APIRouter, Depends
from schemas import UserProject
from models import User, Project
from sqlalchemy.orm import Session
from services import get_current_user
from database import get_db

projects_router = APIRouter(prefix="/projects", tags=["Projects"])


@projects_router.get("/me", response_model=list[UserProject])
def get_all_user_projects(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    projects = db.query(Project).filter((Project.owner_id) == current_user.id).all()
    return projects
