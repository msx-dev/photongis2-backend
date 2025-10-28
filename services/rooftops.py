from sqlalchemy.orm import Session
from models import Rooftop, Project
from schemas import RooftopCreate, ProjectRooftop, RooftopUpdate
from fastapi import HTTPException, status, responses
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


def update_project_rooftop(
    rooftop_id: uuid.UUID, rooftop_data: RooftopUpdate, db: Session
) -> ProjectRooftop:
    rooftop = db.query(Rooftop).filter(Rooftop.id == rooftop_id).first()
    if not rooftop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find this rooftop.",
        )

    for key, value in rooftop_data.model_dump(exclude_unset=True).items():
        setattr(rooftop, key, value)

    db.commit()
    db.refresh(rooftop)
    return rooftop


def delete_project_rooftop(rooftop_id: uuid.UUID, db: Session):
    rooftop = db.query(Rooftop).filter(Rooftop.id == rooftop_id).first()
    if not rooftop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find this rooftop.",
        )

    db.delete(rooftop)
    db.commit()
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
