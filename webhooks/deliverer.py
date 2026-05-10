"""
Webhook delivery helper.

The public API is a single function:

    deliver_webhook(job_id: str, status: str, url: str) -> bool

It validates the URL, posts a JSON payload, and retries on
network or server errors using exponential back‑off.

Raises
------
WebhookDeliveryError
    If the supplied URL is malformed or unsupported.
"""

import json
import logging
import time
from urllib.parse import urlparse
from typing import Final

import requests

# --------------------------------------------------------------------------- #
# Configuration – tweak these constants to change behaviour
# --------------------------------------------------------------------------- #
_MAX_ATTEMPTS: Final[int] = 3          # initial try + retries
_BASE_DELAY: Final[float] = 1.0        # seconds
_BACKOFF_MULTIPLIER: Final[int] = 2   # exponential factor

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #
class WebhookDeliveryError(RuntimeError):
    """Raised when the webhook URL is syntactically invalid or unsupported."""


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _validate_url(url: str) -> None:
    """
    Ensure the URL is a well‑formed HTTP/HTTPS URL.

    Raises
    ------
    WebhookDeliveryError
        If the URL is malformed or uses an unsupported scheme.
    """
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise WebhookDeliveryError(f"Invalid webhook URL: {url}")


def _post_payload(url: str, payload: dict) -> requests.Response:
    """
    Send a POST request with a JSON body.

    Returns
    -------
    requests.Response
        The HTTP response object.
    """
    headers = {"Content-Type": "application/json"}
    return requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def deliver_webhook(*, job_id: str, status: str, url: str) -> bool:
    """
    Deliver a webhook notification about a job's completion status.

    Parameters
    ----------
    job_id : str
        Identifier of the processed job.
    status : str
        Completion status (e.g., "completed", "failed").
    url : str
        Destination webhook URL.

    Returns
    -------
    bool
        ``True`` if the webhook was successfully delivered (HTTP 2xx),
        ``False`` otherwise after exhausting retries.

    Raises
    ------
    WebhookDeliveryError
        If the supplied URL is malformed or unsupported.
    """
    _validate_url(url)

    payload = {"job_id": job_id, "status": status}
    attempt = 0

    while attempt < _MAX_ATTEMPTS:
        try:
            response = _post_payload(url, payload)
            if 200 <= response.status_code < 300:
                logger.info(
                    "Webhook delivered for job %s to %s (status %s)",
                    job_id,
                    url,
                    response.status_code,
                )
                return True
            else:
                logger.warning(
                    "Attempt %d: webhook delivery for job %s failed with status %s",
                    attempt + 1,
                    job_id,
                    response.status_code,
                )
        except requests.RequestException as exc:
            logger.warning(
                "Attempt %d: exception delivering webhook for job %s: %s",
                attempt + 1,
                job_id,
                exc,
            )

        # Exponential back‑off before next retry
        if attempt + 1 < _MAX_ATTEMPTS:
            delay = _BASE_DELAY * (_BACKOFF_MULTIPLIER ** attempt)
            logger.debug("Waiting %.1f seconds before retry", delay)
            time.sleep(delay)

        attempt += 1

    logger.error(
        "All %d webhook delivery attempts failed for job %s to %s",
        _MAX_ATTEMPTS,
        job_id,
        url,
    )
    return False