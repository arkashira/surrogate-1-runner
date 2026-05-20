"""
Email notification service for high‑severity findings.

This module provides a simple SMTP client that sends alert emails
and records delivery status in the `alert_logs` table.

Configuration is read from environment variables:
    SMTP_HOST      - SMTP server hostname
    SMTP_PORT      - SMTP server port (default 587)
    SMTP_USER      - SMTP username (optional)
    SMTP_PASSWORD  - SMTP password (optional)
    EMAIL_FROM     - Default sender email address
    EMAIL_TO       - Default recipient list (comma‑separated)
"""

import os
import smtplib
import logging
from email.message import EmailMessage
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session

# Import the database models and session factory
# (Assumes a `models.py` defining AlertLog and a `db.py` providing get_session)
try:
    from ..models import AlertLog
    from ..db import get_session
except Exception:  # pragma: no cover
    # In case the project structure differs, provide a minimal stub
    AlertLog = None
    get_session = lambda: None

log = logging.getLogger(__name__)

# Environment configuration
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "alerts@axentx.com")
DEFAULT_EMAIL_TO = [addr.strip() for addr in os.getenv("EMAIL_TO", "").split(",") if addr.strip()]


def _get_smtp_connection() -> smtplib.SMTP:
    """
    Create and return an SMTP connection using the configured credentials.
    """
    if not SMTP_HOST:
        raise RuntimeError("SMTP_HOST is not configured")

    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
    smtp.ehlo()
    if SMTP_PORT == 587:
        smtp.starttls()
        smtp.ehlo()
    if SMTP_USER and SMTP_PASSWORD:
        smtp.login(SMTP_USER, SMTP_PASSWORD)
    return smtp


def _build_email_message(
    subject: str,
    body: str,
    to_addresses: List[str],
    cc_addresses: Optional[List[str]] = None,
) -> EmailMessage:
    """
    Construct an EmailMessage object with the given parameters.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(to_addresses)
    if cc_addresses:
        msg["Cc"] = ", ".join(cc_addresses)
    msg.set_content(body)
    return msg


def _log_delivery(session: Session, alert_id: int, success: bool, error: Optional[str] = None) -> None:
    """
    Persist the delivery status in the alert_logs table.
    """
    if AlertLog is None:
        log.debug("AlertLog model not available; skipping log")
        return

    log_entry = AlertLog(
        alert_id=alert_id,
        delivered=success,
        error_message=error,
    )
    session.add(log_entry)
    session.commit()


def send_email(
    alert_payload: Dict[str, Any],
    session: Optional[Session] = None,
) -> None:
    """
    Send an email for the given alert payload.

    Parameters
    ----------
    alert_payload : dict
        Expected keys:
            - alert_id (int)
            - resource_id (str)
            - rule_name (str)
            - severity (str)
            - dashboard_link (str)
            - recipients (list[str]) optional
    session : sqlalchemy.orm.Session, optional
        Database session for logging. If None, a new session is created.

    Raises
    ------
    RuntimeError
        If SMTP configuration is missing or sending fails.
    """
    if session is None:
        session = get_session()

    alert_id = alert_payload.get("alert_id")
    if alert_id is None:
        raise ValueError("alert_payload must contain 'alert_id'")

    recipients = alert_payload.get("recipients") or DEFAULT_EMAIL_TO
    if not recipients:
        raise RuntimeError("No recipients specified for email alert")

    subject = f"[{alert_payload.get('severity', 'UNKNOWN')}] {alert_payload.get('rule_name', 'Unknown Rule')} triggered"
    body = (
        f"Resource ID: {alert_payload.get('resource_id')}\n"
        f"Rule: {alert_payload.get('rule_name')}\n"
        f"Severity: {alert_payload.get('severity')}\n"
        f"Dashboard: {alert_payload.get('dashboard_link')}\n\n"
        f"Alert ID: {alert_id}"
    )

    msg = _build_email_message(subject, body, recipients)

    try:
        smtp = _get_smtp_connection()
        smtp.send_message(msg)
        smtp.quit()
        _log_delivery(session, alert_id, True)
        log.info("Email sent successfully for alert %s", alert_id)
    except Exception as exc:
        _log_delivery(session, alert_id, False, str(exc))
        log.exception("Failed to send email for alert %s", alert_id)
        raise RuntimeError(f"Email delivery failed: {exc}") from exc