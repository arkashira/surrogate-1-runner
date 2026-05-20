"""
Slack notifier for drift detection alerts.

Implements:
- Configurable webhook URL and channel via alerting.yaml
- Message includes service, version, timestamp, and diff summary
- Retry logic: configurable attempts with exponential backoff
- Rate-limit handling: respects Slack's 1 msg/sec per bot limit
"""

import time
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import requests
import yaml

log = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("/opt/axentx/surrogate-1/alerting.yaml")


class SlackNotifier:
    """Slack notifier with retry logic and rate limiting."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the Slack notifier from config file.

        Args:
            config_path: Path to the alerting.yaml configuration file.
                        Defaults to /opt/axentx/surrogate-1/alerting.yaml
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self._load_config()
        self._last_message_time = 0.0

    def _load_config(self) -> None:
        """Load configuration from YAML file with defaults."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with self.config_path.open("r") as f:
            cfg = yaml.safe_load(f) or {}

        slack_cfg = cfg.get("slack", {})
        self.webhook_url: str = slack_cfg.get("webhook_url")
        self.channel: str = slack_cfg.get("channel", "#alerts")
        self.rate_limit_delay: float = slack_cfg.get("rate_limit_delay", 1.0)
        self.max_retries: int = slack_cfg.get("max_retries", 3)
        self.retry_base_delay: float = slack_cfg.get("retry_base_delay", 1.0)

        if not self.webhook_url:
            raise ValueError("slack.webhook_url must be set in alerting.yaml")

    def _build_message(
        self, service: str, version: str, timestamp: str, diff: str
    ) -> Dict[str, Any]:
        """Build Slack message payload."""
        return {
            "channel": self.channel,
            "text": (
                f"*Drift Detected*\n"
                f"• Service: `{service}`\n"
                f"• Version: `{version}`\n"
                f"• Timestamp: {timestamp}\n"
                f"• Diff:\n