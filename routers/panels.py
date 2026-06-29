import uuid
from fastapi import APIRouter, Depends, status
from database import get_db
from services.auth import get_current_user
from sqlalchemy.orm import Session
from schemas import UserPanel, PanelCreate
from models import User
from services import get_user_panels, create_new_user_panel, delete_user_panel


panels_router = APIRouter(prefix="/panels", tags=["Panels"])


@panels_router.get("", response_model=list[UserPanel])
def get_all_user_panels(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_user_panels(current_user, db)


@panels_router.post("", response_model=UserPanel, status_code=status.HTTP_201_CREATED)
def create_new_panel(
    panel: PanelCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_new_user_panel(panel, db, current_user)


@panels_router.delete("/{panel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_panel(
    panel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_user_panel(panel_id, db)
