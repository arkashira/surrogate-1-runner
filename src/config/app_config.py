import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AppConfig:
    """Central application configuration loaded from environment variables."""

    # Centralized logging endpoint (expects JSON POST)
    LOGGING_ENDPOINT: str = os.getenv("AXENTX_LOGGING_ENDPOINT", "http://localhost:9200/ingestion-logs/_doc")

    # Slack webhook for alerting (optional)
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv("AXENTX_SLACK_WEBHOOK_URL")

    # Email alerting configuration (optional)
    EMAIL_SMTP_HOST: Optional[str] = os.getenv("AXENTX_EMAIL_SMTP_HOST")
    EMAIL_SMTP_PORT: int = int(os.getenv("AXENTX_EMAIL_SMTP_PORT", "587"))
    EMAIL_SMTP_USER: Optional[str] = os.getenv("AXENTX_EMAIL_SMTP_USER")
    EMAIL_SMTP_PASSWORD: Optional[str] = os.getenv("AXENTX_EMAIL_SMTP_PASSWORD")
    EMAIL_FROM: Optional[str] = os.getenv("AXENTX_EMAIL_FROM")
    EMAIL_TO: Optional[str] = os.getenv("AXENTX_EMAIL_TO")  # comma-separated list


# Simple lazy singleton pattern
_config_instance: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Return the application configuration, creating it on first call."""
    global _config_instance
    if _config_instance is None:
        _config_instance = AppConfig()
    return _config_instance


# /opt/axentx/surrogate-1/src/logging/logger.py
import json
import logging
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, Optional

import requests

from .config.app_config import get_config


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def _setup_root_logger() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)
    root.setLevel(logging.INFO)


_setup_root_logger()


class AxentxLogger:
    """Utility logger that forwards ingestion job events to the Axentx logging stack
    and raises alerts on failures."""

    def __init__(self, name: str = "axentx.ingestion"):
        self.logger = logging.getLogger(name)
        self.config = get_config()

    def info(self, msg: str, **kwargs: Any) -> None:
        self.logger.info(msg, extra=kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        self.logger.warning(msg, extra=kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        self.logger.error(msg, extra=kwargs)

    def log_job_status(
        self,
        job_id: str,
        status: str,
        *,
        download_speed_mbps: Optional[float] = None,
        upload_time_seconds: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a job status and push a structured record to the centralized logging stack."""
        payload = {
            "job_id": job_id,
            "status": status,
            "download_speed_mbps": download_speed_mbps,
            "upload_time_seconds": upload_time_seconds,
            "details": details or {},
        }

        self.info(f"Ingestion job {job_id} status: {status}", **payload)

        try:
            response = requests.post(
                self.config.LOGGING_ENDPOINT,
                json=payload,
                timeout=5,
            )
            response.raise_for_status()
        except Exception as exc:
            self.error(f"Failed to forward ingestion log for job {job_id}", error=str(exc))

        if status.lower() == "failed":
            self._alert_failure(job_id, payload)

    def _alert_failure(self, job_id: str, payload: Dict[str, Any]) -> None:
        """Send a failure alert via Slack webhook or fallback email."""
        message = f":x: Ingestion job *{job_id}* failed.\nDetails: