"""
Webhook dispatcher with robust retry logic and comprehensive error handling.

This module provides a WebhookDispatcher class that handles webhook notifications
with configurable retry behavior, exponential backoff, and detailed logging.
The payload includes:
- session_id
- status
- error_category (optional)
- resolution_url (optional)

Features:
- Configurable retry count and backoff parameters
- Exponential backoff with jitter
- Comprehensive logging
- Graceful handling of missing webhook URLs
- Timeout configuration
- Customizable headers
"""

import json
import logging
import time
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

log = logging.getLogger(__name__)

class WebhookDispatcher:
    """
    Dispatches webhook notifications with retry logic and exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (default 3).
        backoff_factor: Base backoff factor in seconds (default 1.0).
        initial_delay: Initial delay before first retry (default 1.0s).
        timeout: Request timeout in seconds (default 10.0).
        headers: Default headers to include in requests (default includes Content-Type).
    """

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        initial_delay: float = 1.0,
        timeout: float = 10.0,
        headers: Optional[Dict[str, str]] = None
    ):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay
        self.timeout = timeout
        self.headers = headers or {"Content-Type": "application/json"}

    def _build_payload(
        self,
        session_id: str,
        status: str,
        error_category: Optional[str] = None,
        resolution_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Construct the JSON payload for the webhook.

        Args:
            session_id: Unique identifier for the analysis session.
            status: Current status of the analysis (e.g., "completed").
            error_category: Optional error category if the analysis failed.
            resolution_url: Optional URL pointing to the resolution artifact.

        Returns:
            A dictionary ready to be JSON-encoded.
        """
        payload = {
            "session_id": session_id,
            "status": status,
        }
        if error_category is not None:
            payload["error_category"] = error_category
        if resolution_url is not None:
            payload["resolution_url"] = resolution_url
        return payload

    def dispatch(
        self,
        webhook_url: str,
        session_id: str,
        status: str,
        error_category: Optional[str] = None,
        resolution_url: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Send the webhook payload to the given URL with retry logic.

        Args:
            webhook_url: The target webhook endpoint.
            session_id: Unique identifier for the analysis session.
            status: Current status of the analysis.
            error_category: Optional error category if the analysis failed.
            resolution_url: Optional URL pointing to the resolution artifact.
            custom_headers: Optional additional headers to override defaults.

        Returns:
            True if the webhook was successfully POSTed, False otherwise.

        Note:
            If webhook_url is empty, returns True immediately.
        """
        if not webhook_url:
            log.debug("No webhook URL provided; skipping dispatch.")
            return True

        payload = self._build_payload(session_id, status, error_category, resolution_url)
        headers = {**self.headers, **(custom_headers or {})}
        payload_json = json.dumps(payload)

        attempt = 0
        delay = self.initial_delay

        while attempt <= self.max_retries:
            try:
                log.debug(
                    f"Dispatching webhook attempt {attempt + 1} to {webhook_url} "
                    f"with payload: {payload}"
                )
                response = requests.post(
                    webhook_url,
                    data=payload_json,
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                log.info(f"Webhook dispatched successfully to {webhook_url}")
                return True
            except RequestException as exc:
                attempt += 1
                if attempt > self.max_retries:
                    log.error(
                        f"Webhook dispatch failed after {self.max_retries} retries: {exc}"
                    )
                    return False

                # Add jitter to prevent thundering herd problem
                jitter = (1 + (0.5 * (0.5 - time.time() % 1)))
                backoff = min(delay * self.backoff_factor * jitter, 30)  # Cap at 30s

                log.warning(
                    f"Webhook dispatch attempt {attempt} failed: {exc}. "
                    f"Retrying in {backoff:.1f}s..."
                )
                time.sleep(backoff)
                delay = backoff

        return False