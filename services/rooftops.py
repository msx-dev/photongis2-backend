from sqlalchemy.orm import Session
from models import Rooftop, Project
from schemas import RooftopCreate, ProjectRooftop
from fastapi import HTTPException, status
import uuid


def get_projects_rooftops(project_id: uuid.UUID, db: Session) -> list[Rooftop]:
    rooftops = db.query(Rooftop).filter((Rooftop.project_id) == project_id).all()
    return rooftops


def create_new_rooftop(
    rooftop: RooftopCreate, project_id: uuid.UUID, db: Session
) -> ProjectRooftop:
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can't find project with id '{project_id}'.",
        )

    new_rooftop = Rooftop(**rooftop.model_dump(), project_id=project_id)
    db.add(new_rooftop)
    db.commit()
    db.refresh(new_rooftop)

    return new_rooftop
