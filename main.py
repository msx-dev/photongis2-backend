from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils import create_tables
from routers import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB at start
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=auth_router)
app.include_router(user_router)


@app.get("/health")
def index():
    return "All good."
