import os
import logging
from typing import List

logger = logging.getLogger(__name__)

class ConfigError(RuntimeError):
    """Raised when a required configuration key is missing or malformed."""

def _comma_split(val: str) -> List[str]:
    return [x.strip() for x in val.split(",") if x.strip()]

def load_config():
    """
    Returns a dict with all configuration values.
    Missing optional values are replaced with sensible defaults.
    Missing **required** values raise ConfigError.
    """
    cfg = {}

    # ---------- Email ----------
    cfg["SMTP_SERVER"] = os.getenv("SMTP_SERVER", "localhost")
    cfg["SMTP_PORT"] = int(os.getenv("SMTP_PORT", "587"))
    cfg["SMTP_SENDER"] = os.getenv("NOTIFICATION_SENDER_EMAIL")
    cfg["SMTP_PASSWORD"] = os.getenv("NOTIFICATION_SENDER_PASSWORD")
    cfg["SMTP_RECIPIENTS"] = _comma_split(os.getenv("NOTIFICATION_RECIPIENTS", ""))

    # ---------- Slack ----------
    cfg["SLACK_WEBHOOK_URL"] = os.getenv("SLACK_WEBHOOK_URL")   # optional

    # ---------- Generic webhook ----------
    cfg["WEBHOOK_URL"] = os.getenv("WEBHOOK_URL")               # optional

    # ---------- Global ----------
    cfg["DEFAULT_CHANNELS"] = _comma_split(
        os.getenv("NOTIFICATION_CHANNELS", "console")
    )   # e.g. "email,slack,webhook"

    # Validate required combos
    if "email" in cfg["DEFAULT_CHANNELS"]:
        if not (cfg["SMTP_SENDER"] and cfg["SMTP_PASSWORD"] and cfg["SMTP_RECIPIENTS"]):
            raise ConfigError(
                "Email channel selected but NOTIFICATION_SENDER_EMAIL, "
                "NOTIFICATION_SENDER_PASSWORD, or NOTIFICATION_RECIPIENTS are missing."
            )
    if "slack" in cfg["DEFAULT_CHANNELS"] and not cfg["SLACK_WEBHOOK_URL"]:
        raise ConfigError("Slack channel selected but SLACK_WEBHOOK_URL is missing.")
    if "webhook" in cfg["DEFAULT_CHANNELS"] and not cfg["WEBHOOK_URL"]:
        raise ConfigError("Webhook channel selected but WEBHOOK_URL is missing.")

    logger.debug("Configuration loaded: %s", {k: ("***" if "PASSWORD" in k else v)
                                             for k, v in cfg.items()})
    return cfg