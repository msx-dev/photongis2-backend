import uuid
from fastapi import APIRouter, Depends, status
from schemas import (
    UserProject,
    ProjectCreate,
    ProjectUpdate,
    ProjectRooftop,
    RooftopCreate,
)
from models import User
from sqlalchemy.orm import Session
from schemas.electrical_string import ElectricalString, ElectricalStringCreate
from schemas.project_inverter import ProjectInverter, ProjectInverterCreate
from services import get_current_user
from database import get_db
from services import (
    create_new_user_project,
    update_user_project,
    delete_user_project,
    get_user_project,
    create_new_rooftop,
    get_projects_rooftops,
    delete_user_project_rooftops,
)
from services.projects import add_string_to_inverter, create_project_inverter, delete_projects_inverter, delete_string_from_inverter

projects_router = APIRouter(prefix="/projects", tags=["Projects"])


@projects_router.get("/me", response_model=list[UserProject])
def get_all_user_projects(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_user_project(current_user, db)


@projects_router.post(
    "", response_model=UserProject, status_code=status.HTTP_201_CREATED
)
def create_new_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_user_project(project, db, current_user)


@projects_router.patch("/{project_id}", response_model=UserProject)
def update_project(
    project_id: uuid.UUID,
    project: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user_project(project_id, project, db)


@projects_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_user_project(project_id, db)


@projects_router.delete(
    "/{project_id}/rooftops", status_code=status.HTTP_204_NO_CONTENT
)
def delete_project_rooftops(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_user_project_rooftops(project_id, db)


@projects_router.get("/{project_id}/rooftops", response_model=list[ProjectRooftop])
def get_project_rooftops(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_projects_rooftops(project_id, db)


@projects_router.post(
    "/{project_id}/rooftops",
    response_model=ProjectRooftop,
    status_code=status.HTTP_201_CREATED,
)
def create_project_rooftop(
    project_id: uuid.UUID,
    rooftop: RooftopCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_rooftop(rooftop, project_id, db)


@projects_router.post(
    "/{project_id}/inverters",
    response_model=ProjectInverter,
    status_code=status.HTTP_201_CREATED,
)
def create_project_inverter_endpoint(
    project_id: uuid.UUID,
    payload: ProjectInverterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_project_inverter(project_id, payload, db)

@projects_router.delete(
    "/inverters/{project_inverter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_inverter(
    project_inverter_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_projects_inverter(project_inverter_id, db)

@projects_router.post(
    "/inverters/{project_inverter_id}/strings",
    response_model=ElectricalString,
    status_code=status.HTTP_201_CREATED,
)
def add_electrical_string(
    project_inverter_id: uuid.UUID,
    payload: ElectricalStringCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_string_to_inverter(project_inverter_id, payload, db)

@projects_router.delete(
    "/strings/{string_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_electrical_string(
    string_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_string_from_inverter(string_id, db)