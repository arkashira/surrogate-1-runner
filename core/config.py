import os
from pydantic import BaseSettings, Field, validator

class Settings(BaseSettings):
    """Application‑wide configuration."""

    GITHUB_WEBHOOK_SECRET: str = Field(
        ...,
        env="GITHUB_WEBHOOK_SECRET",
        description="Secret used by GitHub to sign webhook payloads (HMAC‑SHA256).",
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="Python logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    )

    @validator("GITHUB_WEBHOOK_SECRET")
    def secret_must_not_be_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("GITHUB_WEBHOOK_SECRET cannot be empty")
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"          # optional, useful for local dev
        env_file_encoding = "utf-8"

# Export a singleton that can be imported anywhere
settings = Settings()