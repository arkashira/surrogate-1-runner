"""
Utility to compare current request signatures against baseline and
trigger alerts via Slack or email.
"""

import datetime
import json
import smtplib
from email.message import EmailMessage
from typing import Dict, Any, List

from ..config import get_baseline_signatures

# Simple Slack webhook placeholder
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

def send_slack_alert(message: str) -> None:
    if not SLACK_WEBHOOK_URL:
        return
    import requests
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

def send_email_alert(subject: str, body: str) -> None:
    smtp_server = os.getenv("SMTP_SERVER", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", "25"))
    from_addr = os.getenv("ALERT_FROM", "noreply@example.com")
    to_addr = os.getenv("ALERT_TO", "sre@example.com")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    with smtplib.SMTP(smtp_server, smtp_port) as s:
        s.send_message(msg)

def compare_signatures(endpoint: str, current: Dict[str, Any]) -> List[str]:
    """
    Compare current signature dict against baseline.
    Returns a list of changed field paths.
    """
    baseline = get_baseline_signatures().get(endpoint, {})
    changes = []

    def diff_dict(prefix: str, base: Any, curr: Any):
        if isinstance(base, dict) and isinstance(curr, dict):
            for key in set(base.keys()).union(curr.keys()):
                new_prefix = f"{prefix}.{key}" if prefix else key
                if key not in base:
                    changes.append(f"Added field {new_prefix}")
                elif key not in curr:
                    changes.append(f"Removed field {new_prefix}")
                else:
                    diff_dict(new_prefix, base[key], curr[key])
        else:
            if base != curr:
                changes.append(f"Changed {prefix}: {base!r} -> {curr!r}")

    diff_dict("", baseline, current)
    return changes

def alert_on_change(endpoint: str, current: Dict[str, Any]) -> None:
    changes = compare_signatures(endpoint, current)
    if not changes:
        return
    timestamp = datetime.datetime.utcnow().isoformat()
    change_list = "\n".join(changes)
    message = (
        f"⚠️ Signature change detected for endpoint `{endpoint}`\n"
        f"Timestamp: {timestamp}\n"
        f"Changed fields:\n{change_list}"
    )
    send_slack_alert(message)
    send_email_alert(
        subject=f"Signature change: {endpoint}",
        body=message
    )