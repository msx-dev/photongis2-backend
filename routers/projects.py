from fastapi import APIRouter, Depends
from schemas import UserProject, ProjectCreate
from models import User, Project
from sqlalchemy.orm import Session
from services import get_current_user
from database import get_db
from services import create_new_user_project

projects_router = APIRouter(prefix="/projects", tags=["Projects"])


@projects_router.get("/me", response_model=list[UserProject])
def get_all_user_projects(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    projects = db.query(Project).filter((Project.owner_id) == current_user.id).all()
    return projects


@projects_router.post("/create", response_model=UserProject)
def create_new_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_user_project(project, db, current_user)
