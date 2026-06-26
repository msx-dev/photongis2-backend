import uuid
from sqlalchemy.orm import Session, joinedload
from models import User
from schemas import UserProject, ProjectCreate, ProjectUpdate
from models import Project, ProjectInverter, ElectricalString
from fastapi import HTTPException, status, responses

from schemas.electrical_string import ElectricalStringCreate
from schemas.project_inverter import ProjectInverterCreate


def get_user_project(user: User, db: Session) -> list[Project]:
    projects = (
        db.query(Project)
        .filter((Project.owner_id) == user.id)
        .order_by(Project.created_at.asc())
        .all()
    )
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


def update_user_project(
    project_id: uuid.UUID, project_data: ProjectUpdate, db: Session
) -> UserProject:
    project = db.query(Project).filter((Project.id) == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )
    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


def delete_user_project_rooftops(project_id: uuid.UUID, db: Session):
    project = db.query(Project).filter((Project.id) == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )

    for rooftop in project.rooftops:
        db.delete(rooftop)
    db.commit()
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)


def delete_user_project(project_id: uuid.UUID, db: Session):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )
    db.delete(project)
    db.commit()
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)

def create_project_inverter(project_id: uuid.UUID, payload: ProjectInverterCreate, db: Session):
    inverter = ProjectInverter(
        project_id=project_id,
        inverter_id=payload.inverter_id,
    )
    db.add(inverter)
    db.flush()  # get inverter.id without commit

    first_string = ElectricalString(
        project_inverter_id=inverter.id,
        design_lines=payload.electrical_string.design_lines,
        connected_polygons=payload.electrical_string.connected_polygons,
    )

    db.add(first_string)
    db.commit()
    db.refresh(inverter)

    return inverter

def get_project_inverters(project_id: uuid.UUID, db: Session):
    return (
        db.query(ProjectInverter)
        .options(
            joinedload(ProjectInverter.inverter),
            joinedload(ProjectInverter.strings),
        )
        .filter(ProjectInverter.project_id == project_id)
        .all()
    )

def delete_projects_inverter(project_inverter_id: uuid.UUID, db: Session):
    inverter = (
        db.query(ProjectInverter)
        .filter(
            ProjectInverter.id == project_inverter_id
        )
        .first()
    )

    if not inverter:
        raise HTTPException(status_code=404, detail="Project inverter not found")

    db.delete(inverter)
    db.commit()

    return None

def add_string_to_inverter(project_inverter_id: uuid.UUID, payload: ElectricalStringCreate, db: Session):
    string = ElectricalString(
        project_inverter_id=project_inverter_id,
        design_lines=payload.design_lines,
        connected_polygons=payload.connected_polygons,
    )

    db.add(string)
    db.commit()
    db.refresh(string)

    return string

def delete_string_from_inverter(string_id: uuid.UUID, db: Session):
    string = db.query(ElectricalString).filter(ElectricalString.id == string_id).first()

    if not string:
        raise HTTPException(status_code=404, detail="Electrical string not found")

    db.delete(string)
    db.commit()

    return None