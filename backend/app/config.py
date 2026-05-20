from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./simulation.db",
        description="SQLAlchemy database URL",
    )
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()