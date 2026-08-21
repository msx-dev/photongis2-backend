from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils import create_tables
from routers import (
    auth_router,
    user_router,
    projects_router,
    rooftops_router,
    panels_router,
    inverters_router,
    chat_router
)
from fastapi.middleware.cors import CORSMiddleware
from llm.rag.ingestion.indexer import index_manual


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB at start
    create_tables()
    index_manual()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=auth_router)
app.include_router(user_router)
app.include_router(projects_router)
app.include_router(rooftops_router)
app.include_router(panels_router)
app.include_router(inverters_router)
app.include_router(chat_router)

origins = [
    "http://localhost:3000",  # DEV
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def index():
    return "All good."
