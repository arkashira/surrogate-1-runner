
import logging
import smtplib
from email.message import EmailMessage
from typing import List, Dict
from os import environ
from slack_sdk import WebClient

# Configuration
ERROR_RATE_THRESHOLD = 0.05
EMAIL_ADDRESS = "alerts@example.com"
EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD")
TO_EMAIL = "data_scientist@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SLACK_TOKEN = environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "alerts"

logger = logging.getLogger(__name__)

def send_email(subject: str, body: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        try:
            server.send_message(msg)
            logger.info("Email alert sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")

def send_slack_alert(message: str):
    client = WebClient(token=SLACK_TOKEN)
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        logger.info("Slack alert sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send Slack alert: {str(e)}")

def generate_alert_details(problematic_pairs: List[Dict]) -> str:
    details = "Quality Issues Detected:\n"
    for pair in problematic_pairs:
        details += f"Pair ID: {pair.get('id')}, Error Rate: {pair.get('error_rate')}\n"
    return details

def check_error_rate_and_alert(training_pairs: List[Dict]):
    problematic_pairs = [pair for pair in training_pairs if pair.get('error_rate', 0) > ERROR_RATE_THRESHOLD]
    if not problematic_pairs:
        logger.info("No quality issues detected.")
        return

    alert_details = generate_alert_details(problematic_pairs)
    send_email("Quality Issue Alert", alert_details)
    send_slack_alert(alert_details)

# Example usage:
training_pairs = [
    {"id": 1, "error_rate": 0.15},
    {"id": 2, "error_rate": 0.05},
    {"id": 3, "error_rate": 0.2},
]
check_error_rate_and_alert(training_pairs)