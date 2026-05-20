import os
import json
import requests
import smtplib
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from datetime import datetime

# Configuration constants with sensible defaults
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
SMTP_HOST = os.environ.get("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("EMAIL_SENDER")
SMTP_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "alerts@axentx.com")
DEFAULT_EMAIL_TO = os.environ.get("EMAIL_RECIPIENTS", "").split(",")

@dataclass(frozen=True)
class Recommendation:
    """Represents a cost-optimization recommendation with all necessary details."""
    resource_name: str
    current_usage: str
    suggested_action: str
    estimated_savings: float
    currency: str = "USD"
    timestamp: datetime = datetime.now()

def send_slack(message: str, channel: Optional[str] = None) -> bool:
    """Send a message to Slack via webhook with comprehensive error handling."""
    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL not configured, skipping Slack notification")
        return False

    payload = {
        "text": message,
        "username": "cost-optimizer-bot",
        "icon_emoji": ":money_with_wings:"
    }
    if channel:
        payload["channel"] = channel

    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Failed to send Slack message: {e}")
        return False

def send_email(subject: str, body: str, recipients: List[str] = None, html: bool = False) -> bool:
    """Send an email notification with configurable recipients and content type."""
    if recipients is None:
        recipients = DEFAULT_EMAIL_TO

    if not SMTP_USER or not SMTP_PASSWORD or not recipients:
        print("Email not configured, skipping email notification")
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = ", ".join(recipients)

    mime_type = 'html' if html else 'plain'
    msg.attach(MIMEText(body, mime_type))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def format_recommendation(recommendation: Recommendation) -> str:
    """Format a recommendation into a human-readable message."""
    return (
        f"*Cost Optimization Recommendation*\n"
        f"*Resource*: {recommendation.resource_name}\n"
        f"*Current Usage*: {recommendation.current_usage}\n"
        f"*Suggested Action*: {recommendation.suggested_action}\n"
        f"*Estimated Savings*: {recommendation.estimated_savings:.2f} {recommendation.currency}\n"
        f"*Generated*: {recommendation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    )

def notify_recommendation(
    recommendation: Recommendation,
    slack_channel: Optional[str] = None,
    email_recipients: Optional[List[str]] = None,
    channels: List[str] = None
) -> bool:
    """
    Send a cost optimization recommendation via configured channels.

    Args:
        recommendation: The recommendation to send
        slack_channel: Optional Slack channel override
        email_recipients: Optional list of email recipients
        channels: List of channels to use ('slack', 'email'), defaults to both

    Returns:
        bool: True if at least one notification was sent successfully
    """
    if channels is None:
        channels = ['slack', 'email']

    message = format_recommendation(recommendation)
    subject = f"Cost Optimization Recommendation for {recommendation.resource_name}"

    success = False

    if 'slack' in channels:
        success = send_slack(message, slack_channel) or success

    if 'email' in channels:
        success = send_email(subject, message, email_recipients) or success

    return success