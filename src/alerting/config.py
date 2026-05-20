import os
from dataclasses import dataclass
from typing import Optional, List, Literal, Tuple
from functools import lru_cache

Backend = Literal["slack", "email", "none"]


@dataclass(frozen=True, slots=True)
class SlackConfig:
    webhook_url: str
    channel: Optional[str] = None


@dataclass(frozen=True, slots=True)
class EmailConfig:
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    sender: str
    recipient: str
    use_tls: bool = True   # future‑proof flag


@dataclass(frozen=True, slots=True)
class AlertConfig:
    """Central, immutable configuration for the alerting subsystem."""
    backends: Tuple[Backend, ...]          # allow more than one backend
    slack: Optional[SlackConfig] = None
    email: Optional[EmailConfig] = None
    timeout_seconds: int = 60
    retry_attempts: int = 2                # how many times to retry a failing backend
    retry_backoff: float = 1.0             # seconds between retries (exponential later)


def _require(var: str) -> str:
    """Helper that raises a clear error if an env var is missing."""
    val = os.getenv(var)
    if not val:
        raise ValueError(f"Environment variable {var!r} is required for alerting")
    return val


@lru_cache(maxsize=1)               # cache the result – config is static for the process
def load_config() -> AlertConfig:
    """
    Load configuration from environment variables.
    The function is deliberately simple – the surrounding
    infrastructure (Docker/K8s) injects the required values.
    """
    # ------------------------------------------------------------------ #
    # 1️⃣  Choose backends (comma‑separated, case‑insensitive)
    # ------------------------------------------------------------------ #
    raw = os.getenv("ALERT_BACKENDS", "none").lower()
    backends: List[Backend] = [b.strip() for b in raw.split(",") if b.strip()]
    if not backends:
        backends = ["none"]
    # ------------------------------------------------------------------ #
    # 2️⃣  Build per‑backend config objects (only if the backend is requested)
    # ------------------------------------------------------------------ #
    slack_cfg: Optional[SlackConfig] = None
    if "slack" in backends:
        slack_cfg = SlackConfig(
            webhook_url=_require("SLACK_WEBHOOK_URL"),
            channel=os.getenv("SLACK_CHANNEL"),
        )

    email_cfg: Optional[EmailConfig] = None
    if "email" in backends:
        email_cfg = EmailConfig(
            smtp_server=_require("SMTP_SERVER"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            username=_require("SMTP_USERNAME"),
            password=_require("SMTP_PASSWORD"),
            sender=_require("EMAIL_SENDER"),
            recipient=_require("EMAIL_RECIPIENT"),
            use_tls=os.getenv("SMTP_USE_TLS", "true").lower() in {"true", "1", "yes"},
        )

    timeout = int(os.getenv("ALERT_TIMEOUT_SECONDS", "60"))
    retries = int(os.getenv("ALERT_RETRY_ATTEMPTS", "2"))
    backoff = float(os.getenv("ALERT_RETRY_BACKOFF", "1.0"))

    return AlertConfig(
        backends=tuple(backends),   # immutable tuple for safety
        slack=slack_cfg,
        email=email_cfg,
        timeout_seconds=timeout,
        retry_attempts=retries,
        retry_backoff=backoff,
    )