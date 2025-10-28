from sqlalchemy.orm import Session
from models import Rooftop
import uuid


def get_projects_rooftops(project_id: uuid.UUID, db: Session) -> list[Rooftop]:
    rooftops = db.query(Rooftop).filter((Rooftop.project_id) == project_id).all()
    return rooftops
