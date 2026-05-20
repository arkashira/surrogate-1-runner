import os
from dataclasses import dataclass, field
from typing import Dict

@dataclass(frozen=True)
class EmailConfig:
    sender: str
    recipient: str
    smtp_server: str
    smtp_port: int
    username: str
    password: str

@dataclass(frozen=True)
class AlertManagerConfig:
    url: str  # e.g. http://alertmanager:9093/api/v2/alerts

@dataclass(frozen=True)
class AppConfig:
    metrics_port: int = field(default=8000)
    dashboard_port: int = field(default=5000)
    email: EmailConfig = field(default_factory=lambda: EmailConfig(
        sender=os.getenv("EMAIL_FROM", "surrogate-1@example.com"),
        recipient=os.getenv("EMAIL_TO", "admin@example.com"),
        smtp_server=os.getenv("SMTP_SERVER", "smtp.example.com"),
        smtp_port=int(os.getenv("SMTP_PORT", 587)),
        username=os.getenv("SMTP_USER", "user@example.com"),
        password=os.getenv("SMTP_PASS", "password"),
    ))
    alertmanager: AlertManagerConfig = field(default_factory=lambda: AlertManagerConfig(
        url=os.getenv("ALERTMANAGER_URL", "http://alertmanager:9093/api/v2/alerts")
    ))