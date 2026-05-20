import os
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EmailConfig:
    host: str = os.getenv("NOTIF_EMAIL_HOST", "smtp.gmail.com")
    port: int = int(os.getenv("NOTIF_EMAIL_PORT", "587"))
    username: str = os.getenv("NOTIF_EMAIL_USERNAME", "")
    password: str = os.getenv("NOTIF_EMAIL_PASSWORD", "")
    sender: str = os.getenv("NOTIF_EMAIL_SENDER", "")
    recipients: List[str] = os.getenv("NOTIF_EMAIL_RECIPIENTS", "").split(",")


@dataclass(frozen=True)
class SlackConfig:
    webhook_url: str = os.getenv("NOTIF_SLACK_WEBHOOK_URL", "")


@dataclass(frozen=True)
class NotificationConfig:
    email: EmailConfig = EmailConfig()
    slack: SlackConfig = SlackConfig()
    # Toggle handlers – useful for testing / environments
    enable_email: bool = os.getenv("NOTIF_ENABLE_EMAIL", "true").lower() == "true"
    enable_slack: bool = os.getenv("NOTIF_ENABLE_SLACK", "true").lower() == "true"