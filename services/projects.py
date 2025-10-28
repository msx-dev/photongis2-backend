from sqlalchemy.orm import Session
from models import User
from schemas import UserProject, ProjectCreate, ProjectUpdate, ProjectDelete
from models import Project
from fastapi import HTTPException, status, responses


def get_user_project(user: User, db: Session) -> list[Project]:
    projects = db.query(Project).filter((Project.owner_id) == user.id).all()
    return projects


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


def update_user_project(project_data: ProjectUpdate, db: Session) -> UserProject:
    project = db.query(Project).filter((Project.id) == project_data.id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_data.id} not found.",
        )
    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


def delete_user_project(project_data: ProjectDelete, db: Session):
    project = db.query(Project).filter(Project.id == project_data.id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_data.id} not found.",
        )
    db.delete(project)
    db.commit()
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
