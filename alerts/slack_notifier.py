"""Slack notification utility for cost anomaly alerts.

Only HIGH severity anomalies trigger Slack alerts; LOW severity are logged only.
Webhook URL is configurable via surrogate-1.yaml.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

import yaml

logger = logging.getLogger(__name__)


@dataclass
class AlertPayload:
    """Alert payload structure for cost anomalies."""
    provider: str
    service: str
    observed_spend: float
    threshold_breach: float
    severity: str  # "HIGH" or "LOW"
    timestamp: str
    message: str = ""


class SlackNotifier:
    """Slack webhook notifier for cost anomaly alerts."""

    def __init__(self, config_path: str = "/opt/axentx/surrogate-1/surrogate-1.yaml"):
        self.config_path = config_path
        self.webhook_url: Optional[str] = None
        self._load_config()

    def _load_config(self) -> None:
        """Load Slack webhook URL from surrogate-1.yaml configuration."""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)

            # Support nested config structure
            webhook = config.get("alerts", {}).get("slack", {}).get("webhook_url")
            if webhook:
                self.webhook_url = webhook
                logger.info("Slack webhook configured successfully")
            else:
                logger.warning("No Slack webhook URL found in configuration")
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse configuration: {e}")

    def send_alert(self, payload: AlertPayload) -> bool:
        """Send alert to Slack if severity is HIGH.

        Args:
            payload: AlertPayload containing alert details

        Returns:
            True if alert was sent to Slack, False otherwise
        """
        if payload.severity != "HIGH":
            logger.info(f"LOW severity alert logged only: {payload.service}")
            return False

        if not self.webhook_url:
            logger.error("Slack webhook not configured, cannot send HIGH severity alert")
            return False

        try:
            import requests

            message = self._format_message(payload)
            response = requests.post(
                self.webhook_url,
                json={"text": message},
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"Slack alert sent successfully for {payload.service}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False

    def _format_message(self, payload: AlertPayload) -> str:
        """Format alert payload into Slack-compatible message."""
        return (
            f"🚨 *HIGH Severity Cost Anomaly Detected*\n\n"
            f"🏢 Provider: {payload.provider}\n"
            f"🔧 Service: {payload.service}\n"
            f"💰 Observed Spend: ${payload.observed_spend:,.2f}\n"
            f"⚠️ Threshold Breach: ${payload.threshold_breach:,.2f}\n\n"
            f"Timestamp: {payload.timestamp}\n"
            f"Message: {payload.message}"
        )


def create_notifier(config_path: str = "/opt/axentx/surrogate-1/surrogate-1.yaml") -> SlackNotifier:
    """Factory function to create SlackNotifier instance."""
    return SlackNotifier(config_path)