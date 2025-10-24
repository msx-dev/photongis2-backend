import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()  # Reads .env file


class Settings:
    PROJECT_NAME: str = "PhotonGIS_2"
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    DATABASE_TEST_URL: Optional[str] = os.getenv("DATABASE_TEST_URL")
    JWT_SECRET: Optional[str] = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
