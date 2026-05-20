from pathlib import Path
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    policy_dir: Path = Field(default=Path("/opt/axentx/surrogate-1/policy"))
    api_key: str = Field(..., env="POLICY_API_KEY")  # required

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()