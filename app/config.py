import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        default="sqlite:///./cost_data.db",
        env="DATABASE_URL",
        description="SQLAlchemy database URL",
    )
    FORECAST_DAYS_AHEAD: int = Field(default=30, env="FORECAST_DAYS_AHEAD")
    MAPE_THRESHOLD: float = Field(default=5.0, env="MAPE_THRESHOLD")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

settings = Settings()