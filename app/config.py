import yaml
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator

class CollectorConfig(BaseModel):
    type: str = Field(..., description="Collector type (github, jenkins, custom)")
    enabled: bool = Field(True)
    api_url: str
    api_token: str | None = None
    interval_seconds: int = 300
    retention_days: int = 30
    filters: Dict[str, Any] = Field(default_factory=dict)
    webhook_secret: str | None = None

class AppConfig(BaseModel):
    collectors: List[CollectorConfig]
    database_url: str = Field("sqlite+aiosqlite:///./artifacts.db")
    log_level: str = Field("INFO")

    @validator("log_level", pre=True)
    def _normalize_log_level(cls, v):
        return v.upper()

def load_config(path: str | Path) -> AppConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)