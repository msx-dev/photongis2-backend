from models import User, Panel
from sqlalchemy.orm import Session


def get_user_panels(user: User, db: Session) -> list[Panel]:
    panels = db.query(Panel).filter((Panel.owner_id) == user.id).all()
    return panels
