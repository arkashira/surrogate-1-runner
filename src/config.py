from pydantic import BaseSettings

class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    ALERT_LOG_FILE: str = "/var/log/axentx/alerts.log"

    class Config:
        env_file = ".env"

settings = Settings()