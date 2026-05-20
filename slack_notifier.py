"""
Slack notifier for drift‑detection alerts.

Features
--------
* YAML + env‑var configuration (webhook URL, channel)
* Dataclass‑driven, type‑checked payload
* Thread‑safe rate limiting (1 msg / sec)
* 3‑attempt exponential back‑off with 429‑aware handling
* Optional async `notify_async` wrapper
* Fully unit‑testable – HTTP client can be injected
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Protocol

import yaml
import requests

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Configuration helpers
# --------------------------------------------------------------------------- #
DEFAULT_CONFIG_PATH = "/opt/axentx/surrogate-1/config/alerting.yaml"
DEFAULT_CHANNEL = "#drift-alerts"


def _load_yaml_config(path: str) -> Dict[str, Any]:
    """Load a YAML file, returning an empty dict on any error."""
    if not os.path.exists(path):
        logger.debug("Slack config file %s not found – falling back to env vars", path)
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception as exc:  # pragma: no cover – defensive
        logger.warning("Failed to parse Slack config %s: %s", path, exc)
        return {}


# --------------------------------------------------------------------------- #
# Payload definition
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class SlackMessage:
    """Structured representation of a drift‑detection alert."""

    service: str
    version: str
    timestamp: datetime
    diff_summary: str

    def to_payload(self, channel: str) -> Dict[str, Any]:
        """Return the JSON payload expected by a Slack Incoming Webhook."""
        # Slack expects ISO‑8601 timestamps; we always use UTC.
        ts_iso = self.timestamp.astimezone(timezone.utc).isoformat()

        return {
            "channel": channel,
            "username": "Drift Detector",
            "icon_emoji": ":warning:",
            "attachments": [
                {
                    "color": "danger",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f":rotating_light: Drift Detected – {self.service}",
                                "emoji": True,
                            },
                        },
                        {
                            "type": "section",
                            "fields": [
                                {"type": "mrkdwn", "text": f"*Service:*\n{self.service}"},
                                {"type": "mrkdwn", "text": f"*Version:*\n{self.version}"},
                                {"type": "mrkdwn", "text": f"*Timestamp:*\n{ts_iso}"},
                            ],
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Diff Summary:*\n