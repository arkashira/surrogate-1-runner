"""
Alert system integration for surrogate-1.

This module provides a minimal yet functional alert system that:
  * Monitors predefined grid anomalies.
  * Triggers alerts when anomalies are detected.
  * Delivers alerts to designated recipients via email.

The implementation is intentionally lightweight to fit the existing
surrogate-1 codebase and to avoid external dependencies beyond the
Python standard library.
"""

import smtplib
import logging
from email.message import EmailMessage
from typing import List, Dict, Callable, Any

# Configure module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Alert:
    """
    Represents a single alert configuration.

    Attributes:
        name: Human‑readable name of the alert.
        condition: Callable that receives the current grid state and returns
                   True if the alert should fire.
        recipients: List of email addresses to notify.
    """

    def __init__(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool],
        recipients: List[str],
    ):
        self.name = name
        self.condition = condition
        self.recipients = recipients


class AlertSystem:
    """
    Core alert system.

    Usage:
        system = AlertSystem(smtp_server="smtp.example.com", smtp_port=587)
        system.register_alert(Alert(
            name="Overcurrent",
            condition=lambda state: state.get("current") > 1000,
            recipients=["ops@example.com"],
        ))
        system.check_and_notify(state)
    """

    def __init__(self, smtp_server: str, smtp_port: int = 587, smtp_user: str = "", smtp_password: str = ""):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.alerts: List[Alert] = []

    def register_alert(self, alert: Alert) -> None:
        """Register a new alert configuration."""
        logger.debug(f"Registering alert: {alert.name}")
        self.alerts.append(alert)

    def _send_email(self, subject: str, body: str, recipients: List[str]) -> None:
        """Send an email via the configured SMTP server."""
        if not recipients:
            logger.warning("No recipients specified for alert; skipping email.")
            return

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.smtp_user or "alert@surrogate-1.local"
        msg["To"] = ", ".join(recipients)
        msg.set_content(body)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.ehlo()
                if self.smtp_port == 587:
                    smtp.starttls()
                if self.smtp_user and self.smtp_password:
                    smtp.login(self.smtp_user, self.smtp_password)
                smtp.send_message(msg)
            logger.info(f"Alert email sent to {recipients}")
        except Exception as exc:
            logger.error(f"Failed to send alert email: {exc}")

    def check_and_notify(self, grid_state: Dict[str, Any]) -> None:
        """
        Evaluate all registered alerts against the current grid state
        and send notifications for those that trigger.
        """
        for alert in self.alerts:
            try:
                if alert.condition(grid_state):
                    subject = f"[ALERT] {alert.name}"
                    body = f"Alert triggered: {alert.name}\n\nState snapshot:\n{grid_state}"
                    logger.info(f"Triggering alert: {alert.name}")
                    self._send_email(subject, body, alert.recipients)
                else:
                    logger.debug(f"Alert {alert.name} condition not met.")
            except Exception as exc:
                logger.error(f"Error evaluating alert {alert.name}: {exc}")


# Example usage (this block is for demonstration and can be removed or
# adapted by the caller in the surrogate-1 workflow).
if __name__ == "__main__":
    # Dummy grid state for testing
    dummy_state = {"current": 1200, "voltage": 230}

    # Instantiate the system with a local SMTP server (adjust as needed)
    system = AlertSystem(smtp_server="localhost", smtp_port=1025)

    # Register a simple overcurrent alert
    system.register_alert(
        Alert(
            name="Overcurrent",
            condition=lambda state: state.get("current", 0) > 1000,
            recipients=["ops@example.com"],
        )
    )

    # Check and notify
    system.check_and_notify(dummy_state)