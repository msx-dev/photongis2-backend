import uuid

from fastapi import HTTPException, status, responses
from models import User, Panel
from sqlalchemy.orm import Session
from schemas import PanelCreate, UserPanel


def get_user_panels(user: User, db: Session) -> list[Panel]:
    panels = (
        db.query(Panel)
        .filter((Panel.owner_id) == user.id)
        .order_by(Panel.created_at.asc())
        .all()
    )
    return panels


def create_new_user_panel(
    panel: PanelCreate, db: Session, current_user: User
) -> UserPanel:
    db_panel = Panel(
        name=panel.name,
        height=panel.height,
        width=panel.width,  
        power=panel.power,
        vmp=panel.vmp,
        voc=panel.voc,
        imp=panel.imp,
        isc=panel.isc,
        owner_id=current_user.id,
    )
    db.add(db_panel)
    db.commit()
    db.refresh(db_panel)
    return db_panel


def delete_user_panel(panel_id: uuid.UUID, db: Session, current_user: User):
    panel = (
        db.query(Panel)
        .filter(Panel.id == panel_id, Panel.owner_id == current_user.id)
        .first()
    )
    if not panel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Panel with id {panel_id} not found.",
        )
    db.delete(panel)
    db.commit()
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
