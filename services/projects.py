from sqlalchemy.orm import Session
from models import User
from schemas import UserProject, ProjectCreate
from models import Project
from fastapi import HTTPException, status


def create_new_user_project(
    project: ProjectCreate, db: Session, current_user: User
) -> UserProject:
    existing_project = (
        db.query(Project)
        .filter((Project.owner_id) == current_user.id, Project.name == project.name)
        .first()
    )
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with name '{project.name}' already exists.",
        )
    new_project = Project(
        name=project.name,
        owner_id=current_user.id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project
