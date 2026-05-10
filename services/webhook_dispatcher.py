"""
Webhook dispatcher for the surrogate‑1 capture workflow.

The dispatcher is a tiny, stateless helper that POSTs a JSON payload to a
user‑supplied webhook URL once an analysis session finishes.  It is
fully asynchronous, retries on transient failures, and uses an
exponential back‑off strategy (1 s, 2 s, 4 s …).

Why this version?
* **`httpx`** – the most popular async HTTP client, no external
  dependencies beyond the standard library.
* **Explicit payload** – includes `session_id`, `status`,
  optional `error_category`, optional `resolution_url`, and an optional
  human‑readable `summary`.
* **Configurable retry limits** – constants that can be overridden by
  callers if needed.
* **Robust error handling** – logs every failure, raises the original
  exception after the last retry, and never swallows errors silently.
* **Zero side‑effects** – no global state, no external services
  required, and a clean public API.

The module is intentionally lightweight so it can be imported from any
part of the capture pipeline without side‑effects.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

import httpx

# --------------------------------------------------------------------------- #
# Configuration – can be overridden by callers if desired
# --------------------------------------------------------------------------- #
MAX_RETRIES: int = 3
INITIAL_BACKOFF: float = 1.0  # seconds
HTTP_TIMEOUT: float = 10.0  # seconds

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# --------------------------------------------------------------------------- #
# Internal helpers
# --------------------------------------------------------------------------- #
async def _post_with_retry(
    url: str,
    payload: Dict[str, Any],
    *,
    headers: Optional[Dict[str, str]] = None,
    max_retries: int = MAX_RETRIES,
    backoff_factor: float = INITIAL_BACKOFF,
) -> httpx.Response:
    """
    POST ``payload`` to ``url`` with exponential back‑off.

    Parameters
    ----------
    url : str
        Target webhook endpoint.
    payload : dict
        JSON‑serialisable payload.
    headers : dict | None
        Optional HTTP headers.
    max_retries : int
        Number of attempts before giving up.
    backoff_factor : float
        Base back‑off in seconds; doubled after each failure.

    Raises
    ------
    httpx.HTTPError
        If all retry attempts fail.
    """
    backoff = backoff_factor
    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                return response
        except (httpx.HTTPError, httpx.ReadTimeout, httpx.ConnectError) as exc:
            if attempt == max_retries:
                log.error(
                    "Webhook POST failed after %d attempts to %s: %s",
                    attempt,
                    url,
                    exc,
                    exc_info=True,
                )
                raise
            log.warning(
                "Webhook POST attempt %d/%d to %s failed: %s. "
                "Retrying in %.1f s.",
                attempt,
                max_retries,
                url,
                exc,
                backoff,
            )
            await asyncio.sleep(backoff)
            backoff *= 2  # exponential back‑off


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
async def dispatch_webhook(
    webhook_url: str,
    session_id: str,
    status: str,
    *,
    error_category: Optional[str] = None,
    resolution_url: Optional[str] = None,
    summary: Optional[str] = None,
    max_retries: int = MAX_RETRIES,
    backoff_factor: float = INITIAL_BACKOFF,
) -> None:
    """
    Send a webhook notification for a completed analysis session.

    Parameters
    ----------
    webhook_url : str
        The user‑provided webhook endpoint.
    session_id : str
        Identifier of the analysis session.
    status : str
        Current status of the analysis (e.g. ``"completed"`` or ``"failed"``).
    error_category : str | None
        Human‑readable error category if ``status`` indicates failure.
    resolution_url : str | None
        URL where the resolution can be retrieved.
    summary : str | None
        Optional human‑readable summary of the analysis.
    max_retries : int
        Number of retry attempts (default: 3).
    backoff_factor : float
        Base back‑off in seconds (default: 1.0).

    Raises
    ------
    httpx.HTTPError
        If all retry attempts fail.
    """
    if not webhook_url:
        log.debug("No webhook URL provided; skipping dispatch.")
        return

    payload: Dict[str, Any] = {
        "session_id": session_id,
        "status": status,
    }
    if error_category:
        payload["error_category"] = error_category
    if resolution_url:
        payload["resolution_url"] = resolution_url
    if summary:
        payload["summary"] = summary

    headers = {"Content-Type": "application/json"}

    log.info(
        "Dispatching webhook to %s for session %s with status %s",
        webhook_url,
        session_id,
        status,
    )

    await _post_with_retry(
        webhook_url,
        payload,
        headers=headers,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
    )