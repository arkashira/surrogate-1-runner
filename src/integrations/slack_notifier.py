import json
import logging
import threading
from typing import Any, Dict, Optional

import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from ..config.slack_config import SlackConfig

log = logging.getLogger(__name__)


class SlackNotifier:
    """Utility class for sending messages to Slack.

    The notifier is thread-safe and lazily loads its configuration on first use.
    """

    _instance_lock = threading.Lock()
    _instance: Optional["SlackNotifier"] = None

    def __new__(cls) -> "SlackNotifier":
        # Singleton pattern – ensure only one notifier exists per process.
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super(SlackNotifier, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Prevent re-initialisation in the singleton case.
        if hasattr(self, "_initialized") and self._initialized:
            return

        try:
            self.config = SlackConfig.load_from_env()
            self.client = WebClient(token=self.config.bot_token)
            log.debug("SlackNotifier configured with channel %s", self.config.channel)
        except Exception as exc:
            log.error("Failed to load Slack configuration: %s", exc)
            self.config = None  # type: ignore[assignment]

        self._initialized = True

    def _build_base_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "username": self.config.username,
            "icon_emoji": self.config.icon_emoji,
        }
        if self.config.default_channel:
            payload["channel"] = self.config.default_channel
        return payload

    def send_message(self, text: str, channel: Optional[str] = None) -> Optional[str]:
        """Send a simple text message to Slack.

        Args:
            text: The message body.
            channel: Optional override for the target channel.
        """
        if not self.config:
            log.warning("SlackNotifier is disabled because configuration failed to load.")
            return None

        try:
            response = self.client.chat_postMessage(
                channel=channel or self.config.channel,
                text=text,
                **self._build_base_payload(),
            )
            log.debug("Slack message posted successfully: %s", text)
            return response["message"]["ts"]
        except SlackApiError as e:
            log.error("Failed to send Slack notification: %s", e.response["error"])
            return None

    def send_failure_notification(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """Send a formatted failure notification.

        Args:
            error: The exception that triggered the failure.
            context: Additional key-value data to include in the message (e.g. job id).
        """
        text_lines = [
            "*⚠️ Ingestion Failure Detected*",
            f"> *Error*: `{type(error).__name__}` - {str(error)}",
        ]

        if context:
            text_lines.append("*Context:*")
            for key, value in context.items():
                text_lines.append(f"> `{key}`: `{value}`")

        self.send_message("\n".join(text_lines))

    def notify_status_update(self, status: str) -> Optional[str]:
        """Send a status update notification.

        Args:
            status: The status message to send.
        """
        return self.send_message(f"Ingestion status update: {status}")