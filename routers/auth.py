from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from schemas import UserCreate, UserLogin, Token
from utils import create_access_token, create_refresh_token, validate_refresh_token
from database import get_db
from services import create_user, authenticate_user
from models import User

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup", response_model=Token)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user_data)
    # ValueError returned from create_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    access_token = create_access_token({"sub": new_user.email})
    refresh_token = create_refresh_token({"sub": new_user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_router.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)
):
    # Validate refresh token and extract email
    email = validate_refresh_token(refresh_token)

    # Check that user still exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Issue new tokens
    access_token = create_access_token({"sub": user.email})
    new_refresh_token = create_refresh_token({"sub": user.email})

    return {"access_token": access_token, "refresh_token": new_refresh_token}
