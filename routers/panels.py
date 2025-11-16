from fastapi import APIRouter, Depends
from database import get_db
from services.auth import get_current_user
from sqlalchemy.orm import Session
from services import get_user_panels
from schemas import UserPanel
from models import User


panels_router = APIRouter(prefix="/panels", tags=["Panels"])


@panels_router.get("/", response_model=list[UserPanel])
def get_all_user_projects(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_user_panels(current_user, db)
