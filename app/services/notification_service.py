import json
import logging
import smtplib
from email.mime.text import MIMEText
from typing import List, Dict, Any

import requests

from ..config.notification_config import NotificationConfig

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service responsible for sending anomaly alerts via Email and Slack.
    """

    def __init__(self, config: NotificationConfig = None):
        self.config = config or NotificationConfig()

    # --------------------------------------------------------------------- #
    # Email handling
    # --------------------------------------------------------------------- #
    def _send_email(self, subject: str, body: str, recipients: List[str]) -> None:
        if not self.config.enable_email:
            logger.debug("Email notifications are disabled.")
            return

        email_cfg = self.config.email
        if not all([email_cfg.host, email_cfg.port, email_cfg.username,
                    email_cfg.password, email_cfg.sender, recipients]):
            logger.error("Incomplete email configuration; aborting email send.")
            return

        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = email_cfg.sender
        msg["To"] = ", ".join(recipients)

        try:
            with smtplib.SMTP(email_cfg.host, email_cfg.port) as server:
                server.starttls()
                server.login(email_cfg.username, email_cfg.password)
                server.sendmail(email_cfg.sender, recipients, msg.as_string())
            logger.info(f"Email sent to {recipients}")
        except Exception as exc:
            logger.exception(f"Failed to send email notification: {exc}")

    # --------------------------------------------------------------------- #
    # Slack handling
    # --------------------------------------------------------------------- #
    def _send_slack(self, message: str) -> None:
        if not self.config.enable_slack:
            logger.debug("Slack notifications are disabled.")
            return

        webhook_url = self.config.slack.webhook_url
        if not webhook_url:
            logger.error("Slack webhook URL not configured; aborting Slack send.")
            return

        payload = {"text": message}
        try:
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            logger.info("Slack notification sent successfully.")
        except Exception as exc:
            logger.exception(f"Failed to send Slack notification: {exc}")

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def notify_anomaly(self, anomaly: Dict[str, Any]) -> None:
        """
        Send a formatted anomaly alert via the enabled channels.

        Expected `anomaly` dict keys:
            - budget (float)
            - actual_spend (float)
            - period_days (int)
            - top_cost_drivers (list of dicts with 'name' and 'cost')
        """
        subject = "🚨 Cost Anomaly Detected"
        body = self._format_message(anomaly)

        # Email
        email_recipients = self.config.email.recipients
        if email_recipients:
            self._send_email(subject, body, email_recipients)

        # Slack
        self._send_slack(body)

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #
    @staticmethod
    def _format_message(anomaly: Dict[str, Any]) -> str:
        budget = anomaly.get("budget", 0)
        actual = anomaly.get("actual_spend", 0)
        period = anomaly.get("period_days", 7)
        drivers = anomaly.get("top_cost_drivers", [])

        header = (
            f"*Cost Anomaly Detected*\n"
            f"Period: Last {period} days\n"
            f"Budget: ${budget:,.2f}\n"
            f"Actual Spend: ${actual:,.2f} ({(actual / budget * 100 if budget else 0):.1f}% of budget)\n"
        )

        driver_lines = "\n".join(
            [
                f"{i + 1}. {d.get('name', 'Unknown')} – ${d.get('cost', 0):,.2f}"
                for i, d in enumerate(drivers[:3])
            ]
        )
        if driver_lines:
            driver_section = f"\n*Top 3 Cost Drivers:*\n{driver_lines}"
        else:
            driver_section = ""

        return f"{header}{driver_section}"