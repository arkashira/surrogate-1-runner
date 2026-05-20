import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Core
    provider: str = Field("azure", env="COST_PROVIDER")
    # Azure
    subscription_id: str = Field(..., env="AZURE_SUBSCRIPTION_ID")
    tenant_id: str = Field(..., env="AZURE_TENANT_ID")
    client_id: str = Field(..., env="AZURE_CLIENT_ID")
    client_secret: str = Field(..., env="AZURE_CLIENT_SECRET")
    # DB
    audit_db_url: str = Field(..., env="AUDIT_DB_URL")
    # Cache
    redis_url: str = Field(..., env="REDIS_URL")
    # Prometheus
    prometheus_port: int = Field(8001, env="PROMETHEUS_PORT")

settings = Settings()