from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils import create_tables

@asynccontextmanager
async def lifespan(app:FastAPI):
    #Initialize DB at start
    create_tables()
    yield


app = FastAPI()

@app.get("/health")
def index():
    return {"status":"All good. Running ..."} 