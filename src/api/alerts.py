"""
Flask blueprint providing alert configuration and trigger endpoints.
The module implements:
  * GET /api/alerts/settings   – Retrieve current threshold settings per provider.
  * POST /api/alerts/settings  – Update threshold for a provider.
  * POST /api/alerts/trigger   – Trigger an alert if cost exceeds threshold * 7‑day average.
The alerting logic sends an email via SMTP and a Slack message via a webhook.
"""

import os
import json
import smtplib
from email.message import EmailMessage
from typing import Dict

import requests
from flask import Blueprint, request, jsonify, current_app

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
# Environment variables for email and Slack integration
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "localhost")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "25"))
EMAIL_FROM = os.getenv("EMAIL_FROM", "alerts@axentx.com")
EMAIL_TO = os.getenv("EMAIL_TO", "ops@axentx.com")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Default threshold multiplier (2x) if not configured per provider
DEFAULT_THRESHOLD = 2.0

# In‑memory store for provider thresholds.
# In production this would be persisted in a database or config file.
_provider_thresholds: Dict[str, float] = {}


# --------------------------------------------------------------------------- #
# Flask Blueprint
# --------------------------------------------------------------------------- #
alerts_bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")


@alerts_bp.route("/settings", methods=["GET"])
def get_settings():
    """
    Return the current threshold settings for all providers.
    """
    return jsonify(_provider_thresholds)


@alerts_bp.route("/settings", methods=["POST"])
def update_settings():
    """
    Update the threshold for a specific provider.
    Expected JSON body: { "provider": "<name>", "threshold": <float> }
    """
    data = request.get_json()
    if not data or "provider" not in data or "threshold" not in data:
        return jsonify({"error": "Missing provider or threshold"}), 400

    provider = data["provider"]
    try:
        threshold = float(data["threshold"])
    except (TypeError, ValueError):
        return jsonify({"error": "Threshold must be a number"}), 400

    _provider_thresholds[provider] = threshold
    return jsonify({"message": f"Threshold for {provider} set to {threshold}"}), 200


def _send_email(subject: str, body: str):
    """
    Send an email using the configured SMTP server.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as smtp:
        smtp.send_message(msg)


def _send_slack(message: str):
    """
    Post a message to Slack via webhook.
    """
    if not SLACK_WEBHOOK_URL:
        current_app.logger.warning("SLACK_WEBHOOK_URL not configured; skipping Slack notification")
        return

    payload = {"text": message}
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as e:
        current_app.logger.error(f"Failed to send Slack message: {e}")


@alerts_bp.route("/trigger", methods=["POST"])
def trigger_alert():
    """
    Endpoint to evaluate a cost against the provider's threshold.
    Expected JSON body:
      {
        "provider": "<name>",
        "cost": <float>,
        "average_7d": <float>
      }
    If cost > threshold * average_7d, an email and Slack alert are sent.
    """
    data = request.get_json()
    required = {"provider", "cost", "average_7d"}
    if not data or not required.issubset(data):
        return jsonify({"error": f"Missing fields: {required}"}), 400

    provider = data["provider"]
    try:
        cost = float(data["cost"])
        avg = float(data["average_7d"])
    except (TypeError, ValueError):
        return jsonify({"error": "cost and average_7d must be numbers"}), 400

    threshold = _provider_thresholds.get(provider, DEFAULT_THRESHOLD)
    if cost > threshold * avg:
        subject = f"[ALERT] {provider} cost spike detected"
        body = (
            f"Provider: {provider}\n"
            f"Current cost: ${cost:,.2f}\n"
            f"7‑day average: ${avg:,.2f}\n"
            f"Threshold multiplier: {threshold}x\n"
            f"Action required!"
        )
        _send_email(subject, body)
        _send_slack(body)
        return jsonify({"alert_sent": True, "message": "Alert dispatched"}), 200
    else:
        return jsonify({"alert_sent": False, "message": "No alert; cost within threshold"}), 200