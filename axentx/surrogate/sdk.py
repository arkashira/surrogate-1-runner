"""
Axentx Surrogate SDK – thin wrapper around the Surrogate HTTP API.

Only one public helper is currently provided:

* ``run_workflow`` – submit a workflow definition and obtain a correlation ID.
"""

from __future__ import annotations

import json
from typing import Any, Dict

import requests


class SurrogateError(Exception):
    """
    Raised when the Surrogate API returns a non‑2xx response.

    Attributes
    ----------
    message: str
        Human‑readable error message (usually the ``error`` field from the API).
    payload: dict
        The workflow definition that was sent to the server.
    status_code: int
        HTTP status code returned by the server.
    response_body: Any
        Raw JSON (or text) body returned by the server – useful for debugging.
    """

    def __init__(
        self,
        message: str,
        payload: Dict[str, Any],
        status_code: int,
        response_body: Any,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.payload = payload
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:  # pragma: no cover – trivial
        return f"{self.message} (status {self.status_code})"


def _post_json(url: str, json_payload: Dict[str, Any]) -> requests.Response:
    """
    Small internal helper that centralises request construction.
    Makes it easier to mock in tests and to change headers in one place.
    """
    headers = {"Content-Type": "application/json"}
    return requests.post(url, json=json_payload, headers=headers)


def run_workflow(definition: Dict[str, Any]) -> str:
    """
    Submit a workflow definition to the Surrogate platform.

    Parameters
    ----------
    definition:
        The workflow definition as a plain ``dict``.  It is **not** mutated.

    Returns
    -------
    str
        The ``correlation_id`` returned by the API – this can be used to poll
        status or retrieve logs.

    Raises
    ------
    SurrogateError
        If the HTTP request does not return a 2xx status code.  The exception
        contains the original payload, the status code and the error message
        (or the raw body if the server did not return JSON).

    Example
    -------
    >>> from axentx.surrogate.sdk import run_workflow, SurrogateError
    >>> try:
    ...     cid = run_workflow({"name": "demo", "steps": []})
    ...     print("started:", cid)
    ... except SurrogateError as exc:
    ...     print("failed:", exc)
    """
    url = "https://api.surrogate.axentx.com/workflows"

    # Perform the request – any network‑level exception (e.g. timeout) will
    # propagate as a ``requests`` exception; callers can catch it if they wish.
    response = _post_json(url, definition)

    # Successful 2xx → extract correlation_id.
    if 200 <= response.status_code < 300:
        try:
            return response.json()["correlation_id"]
        except (ValueError, KeyError) as exc:  # pragma: no cover – defensive
            raise SurrogateError(
                "Malformed success response",
                payload=definition,
                status_code=response.status_code,
                response_body=response.text,
            ) from exc

    # Failure → try to pull a useful error message from the body.
    try:
        body = response.json()
        message = body.get("error", "Unknown error")
    except ValueError:  # not JSON – fall back to raw text
        body = response.text
        message = body or "Unknown error"

    raise SurrogateError(
        message=message,
        payload=definition,
        status_code=response.status_code,
        response_body=body,
    )