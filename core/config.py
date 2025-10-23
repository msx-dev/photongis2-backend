import os
from dotenv import load_dotenv

load_dotenv()  # Reads .env file


class Settings:
    PROJECT_NAME: str = "My FastAPI App"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
