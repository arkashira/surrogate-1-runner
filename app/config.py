import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./scheduler.db")
    API_KEY: str = os.getenv("API_KEY", "supersecret")
    RUNNER_ENDPOINT: str = os.getenv("RUNNER_ENDPOINT", "http://localhost:8000/workflows/run")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()