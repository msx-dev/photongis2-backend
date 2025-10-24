from fastapi.testclient import TestClient
from dotenv import load_dotenv
from core import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db

load_dotenv()

engine = create_engine(settings.DATABASE_TEST_URL)  # type: ignore

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "All good."
