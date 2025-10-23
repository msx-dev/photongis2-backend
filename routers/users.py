from fastapi import APIRouter, Depends
from schemas import UserOutput
from models import User
from services import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/me", response_model=UserOutput)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
