import os
import yaml
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class EmailSettings:
    smtp_server: str = "localhost"
    smtp_port: int = 1025
    sender_email: str = "noreply@axentx.com"
    sendgrid_api_key: Optional[str] = None
    use_tls: bool = False
    timeout_seconds: int = 30
    max_retries: int = 2
    retry_backoff_seconds: float = 1.0


@dataclass
class NotificationToggles:
    """All possible event types are optional – missing keys are treated as disabled."""
    toggles: Dict[str, bool] = field(default_factory=dict)


@dataclass
class AppConfig:
    email: EmailSettings
    notifications: NotificationToggles

    @staticmethod
    def _load_yaml(path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    @classmethod
    def from_file(cls, path: str = "config.yaml") -> "AppConfig":
        raw = cls._load_yaml(path)

        # Environment overrides (most useful for secrets)
        env_overrides = {
            "email": {
                "smtp_server": os.getenv("SMTP_SERVER"),
                "smtp_port": os.getenv("SMTP_PORT"),
                "sender_email": os.getenv("SENDER_EMAIL"),
                "sendgrid_api_key": os.getenv("SENDGRID_API_KEY"),
                "use_tls": os.getenv("SMTP_USE_TLS"),
                "timeout_seconds": os.getenv("SMTP_TIMEOUT"),
                "max_retries": os.getenv("EMAIL_MAX_RETRIES"),
                "retry_backoff_seconds": os.getenv("EMAIL_RETRY_BACKOFF"),
            },
            "notifications": {
                # Example: NOTIFY_DATA_INGEST_COMPLETE=true
                # All keys are lower‑cased and prefixed with NOTIFY_
                **{
                    key.lower(): os.getenv(f"NOTIFY_{key.upper()}", "false").lower()
                    == "true"
                    for key in raw.get("notifications", {})
                }
            },
        }

        # Merge YAML + env (env wins when not None)
        email_cfg = {**raw.get("email", {}), **{k: v for k, v in env_overrides["email"].items() if v is not None}}
        notif_cfg = {**raw.get("notifications", {}), **{k: v for k, v in env_overrides["notifications"].items() if isinstance(v, bool)}}

        # Cast types that come from env (they are strings)
        if isinstance(email_cfg.get("smtp_port"), str):
            email_cfg["smtp_port"] = int(email_cfg["smtp_port"])
        if isinstance(email_cfg.get("use_tls"), str):
            email_cfg["use_tls"] = email_cfg["use_tls"].lower() == "true"
        if isinstance(email_cfg.get("timeout_seconds"), str):
            email_cfg["timeout_seconds"] = int(email_cfg["timeout_seconds"])
        if isinstance(email_cfg.get("max_retries"), str):
            email_cfg["max_retries"] = int(email_cfg["max_retries"])
        if isinstance(email_cfg.get("retry_backoff_seconds"), str):
            email_cfg["retry_backoff_seconds"] = float(email_cfg["retry_backoff_seconds"])

        return cls(
            email=EmailSettings(**email_cfg),
            notifications=NotificationToggles(toggles=notif_cfg),
        )