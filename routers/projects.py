from fastapi import APIRouter, Depends, status
from schemas import UserProject, ProjectCreate, ProjectUpdate, ProjectDelete
from models import User
from sqlalchemy.orm import Session
from services import get_current_user
from database import get_db
from services import (
    create_new_user_project,
    update_user_project,
    delete_user_project,
    get_user_project,
)

projects_router = APIRouter(prefix="/projects", tags=["Projects"])


@projects_router.get("/me", response_model=list[UserProject])
def get_all_user_projects(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_user_project(current_user, db)


@projects_router.post("/create", response_model=UserProject)
def create_new_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_user_project(project, db, current_user)


@projects_router.patch("/update", response_model=UserProject)
def update_project(
    project: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user_project(project, db)


@projects_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project: ProjectDelete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_user_project(project, db)
