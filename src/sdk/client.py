"""
Thin wrapper around the Surrogate pricing‑validation HTTP endpoint.

The endpoint is expected to be:
    POST {base_url}/pricing/validate
with a JSON body that contains the product description.

Authentication is performed via the ``Authorization: Bearer <API_KEY>`` header.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests


class SurrogateAPIError(RuntimeError):
    """Raised when the Surrogate API returns a non‑successful response."""


class SurrogateClient:
    """
    Minimal, test‑friendly client for the Surrogate pricing‑validation service.

    Parameters
    ----------
    base_url: str, optional
        The root URL of the API.  Defaults to the public production endpoint.
        Can be overridden with the ``SURROGATE_API_URL`` environment variable
        (useful for staging or CI).
    timeout: int | float, optional
        HTTP request timeout in seconds.  Default = 15 s.
    """

    def __init__(self, base_url: str | None = None, timeout: int | float = 15) -> None:
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise RuntimeError(
                "API_KEY environment variable is required for Surrogate API calls"
            )

        # Allow the caller (or CI) to point at a different host.
        env_url = os.getenv("SURROGATE_API_URL")
        self.base_url = (env_url or base_url or "https://api.surrogate.axentx.com").rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.timeout = timeout

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def validate_pricing(self, product_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the pricing‑validation endpoint.

        Parameters
        ----------
        product_json: dict
            The product description that will be sent verbatim to the API.

        Returns
        -------
        dict
            Parsed JSON response from the API.

        Raises
        ------
        SurrogateAPIError
            If the HTTP status is not 2xx or the response body cannot be parsed.
        """
        url = f"{self.base_url}/pricing/validate"
        response = requests.post(
            url,
            headers=self.headers,
            json=product_json,
            timeout=self.timeout,
        )

        if not response.ok:
            # Try to surface a helpful message from the API payload.
            try:
                err_detail = response.json().get("error", response.text)
            except Exception:
                err_detail = response.text
            raise SurrogateAPIError(
                f"Pricing validation failed (status {response.status_code}): {err_detail}"
            )

        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise SurrogateAPIError(f"Invalid JSON response from API: {exc}") from exc