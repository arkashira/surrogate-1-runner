"""
Simple notification service for the surrogate-1 dashboard.

Supports sending emails via SMTP and Slack messages via webhook.
Configuration is read from environment variables:

EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_FROM
SLACK_WEBHOOK_URL
"""

import os
import smtplib
import ssl
from email.message import EmailMessage
import json
import requests
from typing import Optional, Dict, Any


class NotificationError(Exception):
    """Raised when a notification fails to send."""


class NotificationService:
    """
    A lightweight notification service that can send emails and Slack messages.
    """

    def __init__(
        self,
        email_config: Optional[Dict[str, Any]] = None,
        slack_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the service.

        :param email_config: Optional dict with keys host, port, user, pass, from_addr.
        :param slack_config: Optional dict with key webhook_url.
        """
        # Load defaults from environment
        self.email_config = email_config or {
            "host": os.getenv("EMAIL_HOST", "localhost"),
            "port": int(os.getenv("EMAIL_PORT", "25")),
            "user": os.getenv("EMAIL_USER"),
            "pass": os.getenv("EMAIL_PASS"),
            "from_addr": os.getenv("EMAIL_FROM", "noreply@axentx.com"),
        }
        self.slack_config = slack_config or {
            "webhook_url": os.getenv("SLACK_WEBHOOK_URL")
        }

    # ----------------------------------------------------------------------
    # Email helpers
    # ----------------------------------------------------------------------
    def _build_email(self, to: str, subject: str, body: str) -> EmailMessage:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email_config["from_addr"]
        msg["To"] = to
        msg.set_content(body)
        return msg

    def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Send an email using the configured SMTP server.

        Raises NotificationError on failure.
        """
        msg = self._build_email(to, subject, body)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.email_config["host"], self.email_config["port"]) as server:
                if self.email_config["user"] and self.email_config["pass"]:
                    server.starttls(context=context)
                    server.login(self.email_config["user"], self.email_config["pass"])
                server.send_message(msg)
        except Exception as exc:
            raise NotificationError(f"Failed to send email: {exc}") from exc

    # ----------------------------------------------------------------------
    # Slack helpers
    # ----------------------------------------------------------------------
    def send_slack(self, channel: str, message: str) -> None:
        """
        Send a message to a Slack channel via webhook.

        Raises NotificationError on failure.
        """
        if not self.slack_config["webhook_url"]:
            raise NotificationError("Slack webhook URL not configured")

        payload = {
            "channel": channel,
            "text": message,
        }
        try:
            resp = requests.post(
                self.slack_config["webhook_url"],
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
            resp.raise_for_status()
        except Exception as exc:
            raise NotificationError(f"Failed to send Slack message: {exc}") from exc

    # ----------------------------------------------------------------------
    # Unified notification
    # ----------------------------------------------------------------------
    def notify(self, recipients: Dict[str, str], message: str) -> None:
        """
        Send notifications to a mix of email and Slack recipients.

        :param recipients: dict mapping recipient type to address.
            Supported keys: 'email', 'slack'.
        :param message: The message body.
        """
        if "email" in recipients:
            self.send_email(recipients["email"], "Surrogate-1 Notification", message)
        if "slack" in recipients:
            self.send_slack(recipients["slack"], message)