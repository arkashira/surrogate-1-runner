import os
from dotenv import load_dotenv

load_dotenv()  # pulls .env into os.environ

class Config:
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_APP_TOKEN: str = os.getenv("SLACK_APP_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")
    SLACK_TASK_CHANNEL_ID: str = os.getenv("SLACK_TASK_CHANNEL_ID", "")
    SLACK_PORT: int = int(os.getenv("SLACK_PORT", "3000"))
    SLACK_SOCKET_MODE: bool = os.getenv("SLACK_SOCKET_MODE", "true").lower() in ("true", "1")