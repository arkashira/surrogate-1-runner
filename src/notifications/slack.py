# src/notifications/slack.py
from __future__ import annotations

import json
import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Optional

import requests

logger = logging.getLogger(__name__)


# Best-effort mapping: email local-part -> Slack handle (without @)
# Replace with a real directory/identity lookup in production.
def _email_to_slack_mention(email: Optional[str]) -> Optional[str]:
    if not email:
        return None
    local = email.strip().split("@")[0].lower()
    handle = re.sub(r"[^a-z0-9\-_]", "", local)
    return f"@{handle}" if handle else None


@dataclass(frozen=True)
class StatusChange:
    request_title: str
    new_status: str
    public_url: str
    sla_timer_seconds: Optional[int] = None
    requester_email: Optional[str] = None
    request_id: Optional[str] = None


class SlackNotifier:
    """
    Post status changes to Slack via incoming webhook with exponential backoff retry.

    Behavior:
    - Returns True only on HTTP 2xx.
    - Retries on network errors and 5xx (max_retries, exponential backoff).
    - Does NOT retry on 4xx (treated as permanent client errors).
    - Raises only on unrecoverable programming errors.
    """

    def __init__(
        self,
        webhook_url: str,
        channel: Optional[str] = None,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        timeout: float = 10.0,
    ) -> None:
        if not webhook_url:
            raise ValueError("webhook_url is required")
        self.webhook_url = webhook_url
        self.channel = channel
        self.max_retries = max(1, int(max_retries))
        self.backoff_factor = float(backoff_factor)
        self.timeout = float(timeout)

    def notify_status_change(self, change: StatusChange) -> bool:
        payload = self._build_payload(change)
        last_exception: Optional[Exception] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.post(
                    self.webhook_url,
                    json=payload,
                    timeout=self.timeout,
                    headers={"Content-Type": "application/json"},
                )
                if 200 <= resp.status_code < 300:
                    logger.info(
                        "Slack notification sent for request=%s status=%s",
                        change.request_id or change.request_title,
                        change.new_status,
                    )
                    return True

                # Permanent client errors: do not retry
                if 400 <= resp.status_code < 500:
                    logger.error(
                        "Slack webhook client error (status=%s): %s",
                        resp.status_code,
                        resp.text,
                    )
                    return False

                # Transient server errors or unexpected codes: retry
                logger.warning(
                    "Slack webhook attempt %s/%s failed (status=%s): %s",
                    attempt,
                    self.max_retries,
                    resp.status_code,
                    resp.text,
                )
            except (requests.Timeout, requests.ConnectionError) as exc:
                logger.warning(
                    "Slack webhook attempt %s/%s network error: %s",
                    attempt,
                    self.max_retries,
                    exc,
                )
                last_exception = exc
            except Exception as exc:
                logger.exception("Unexpected error posting to Slack")
                last_exception = exc

            if attempt < self.max_retries:
                sleep_
