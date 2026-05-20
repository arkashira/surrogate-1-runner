from pydantic import BaseSettings, AnyHttpUrl, Field

class Settings(BaseSettings):
    costinel_api_url: AnyHttpUrl = Field(
        "https://api.costinel.com", env="COSTINEL_API_URL"
    )
    costinel_api_key: str = Field(..., env="COSTINEL_API_KEY")
    db_dsn: str = Field(..., env="DATABASE_DSN")          # e.g. postgresql://user:pw@host/db
    max_retries: int = Field(3, env="COSTINEL_MAX_RETRIES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()