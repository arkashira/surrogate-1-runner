import smtplib
from email.message import EmailMessage
from typing import List
import os
from src.dashboard.alerts_display import Alert, AlertStore

# Configuration with environment variables
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
ALERT_RECIPIENTS = os.getenv("ALERT_RECIPIENTS", "alerts@example.com").split(",")

def send_email(subject: str, body: str, recipients: List[str]) -> None:
    """Send a plain-text email with error handling."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER or "noreply@example.com"
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            if SMTP_USER and SMTP_PASS:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def notify_new_alert(alert: Alert, store: AlertStore) -> None:
    """Notify via email when a new alert is added with recent history."""
    recent = store.all()
    body_lines = [
        f"New budget alert for model {alert.model} at endpoint {alert.endpoint}",
        f"Usage: {alert.usage:.2f}, Budget: {alert.budget:.2f}",
        f"Timestamp: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Recent alerts:",
    ]
    body_lines.extend(render_alerts(recent))
    body = "\n".join(body_lines)

    send_email(
        subject=f"Budget Alert: {alert.model} ({alert.endpoint})",
        body=body,
        recipients=ALERT_RECIPIENTS
    )

def add_and_notify(alert: Alert, store: AlertStore) -> None:
    """Add an alert to the store and send an email notification."""
    store.add(alert)
    notify_new_alert(alert, store)