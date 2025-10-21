from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/login")
def login():
    return {"data":"login"}

@auth_router.post("/signup")
def signup():
    return {"data":"signed up"}