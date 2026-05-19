from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    # ------------------------------------------------------------------ #
    # Database
    # ------------------------------------------------------------------ #
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./surrogate.db",
        env="DATABASE_URL",
        description="SQLAlchemy async URL – e.g. postgres+asyncpg://user:pw@host/db"
    )

    # ------------------------------------------------------------------ #
    # Rate limiting
    # ------------------------------------------------------------------ #
    RATE_LIMIT: int = Field(default=100, env="RATE_LIMIT")
    RATE_PERIOD: int = Field(default=60, env="RATE_PERIOD")   # seconds

    # ------------------------------------------------------------------ #
    # Redis (optional)
    # ------------------------------------------------------------------ #
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    # If REDIS_URL is set we use Redis for the counter, otherwise we fall back
    # to a process‑local in‑memory store.

    # ------------------------------------------------------------------ #
    # API‑key store (demo)
    # ------------------------------------------------------------------ #
    # In a real system you would keep keys in a DB table.  For a quick start
    # we allow a hard‑coded set that can be overridden via env var.
    VALID_API_KEYS: str = Field(
        default="supersecretkey123",
        env="VALID_API_KEYS",
        description="Comma‑separated list of keys that are accepted."
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()