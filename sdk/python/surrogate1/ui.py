"""
UI Automation helper for Surrogate‑1 SDK.

This module adds new UI automation methods while preserving the
v0.9.x API surface.  All requests are authenticated via the existing
API key system and are routed to the standard Surrogate‑1 API
endpoint.  The implementation is intentionally lightweight so that
it can be dropped into the current SDK without affecting other
components.

Usage:

    from surrogate1.ui import UIAutomation
    ui = UIAutomation(api_key="YOUR_API_KEY")
    test_id = ui.start_test("login_flow", {"browser": "chrome"})
    status = ui.get_status(test_id)
    ui.stop_test(test_id)
"""

import json
import requests
from typing import Any, Dict, Optional

# Default base URL for the Surrogate‑1 API.  Tests or deployments can
# override this by passing a custom `base_url` to the constructor.
DEFAULT_BASE_URL = "https://api.surrogate1.com"


class UIAutomation:
    """
    UI Automation client.

    Parameters
    ----------
    api_key : str
        The API key used for authentication.
    base_url : str, optional
        Base URL of the Surrogate‑1 API.  Defaults to
        ``DEFAULT_BASE_URL``.
    """

    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # ------------------------------------------------------------------
    # New v1.x methods
    # ------------------------------------------------------------------
    def start_test(self, test_name: str, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Start a new UI automation test.

        Parameters
        ----------
        test_name : str
            Human‑readable name of the test.
        config : dict, optional
            Configuration options for the test runner.

        Returns
        -------
        str
            The unique identifier of the started test.
        """
        payload = {"name": test_name, "config": config or {}}
        resp = requests.post(
            f"{self.base_url}/ui/tests",
            headers=self._headers,
            data=json.dumps(payload),
        )
        resp.raise_for_status()
        return resp.json()["test_id"]

    def stop_test(self, test_id: str) -> None:
        """
        Stop a running UI automation test.

        Parameters
        ----------
        test_id : str
            Identifier of the test to stop.
        """
        resp = requests.post(
            f"{self.base_url}/ui/tests/{test_id}/stop",
            headers=self._headers,
        )
        resp.raise_for_status()

    def get_status(self, test_id: str) -> Dict[str, Any]:
        """
        Retrieve the status of a UI automation test.

        Parameters
        ----------
        test_id : str
            Identifier of the test.

        Returns
        -------
        dict
            Status information returned by the API.
        """
        resp = requests.get(
            f"{self.base_url}/ui/tests/{test_id}",
            headers=self._headers,
        )
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Backward‑compatibility wrappers (v0.9.x)
    # ------------------------------------------------------------------
    def run_ui_test(self, test_name: str, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Legacy alias for :meth:`start_test`.

        This method exists to preserve the public API of v0.9.x.
        """
        return self.start_test(test_name, config)

    def cancel_ui_test(self, test_id: str) -> None:
        """
        Legacy alias for :meth:`stop_test`.

        This method exists to preserve the public API of v0.9.x.
        """
        self.stop_test(test_id)

    def ui_test_status(self, test_id: str) -> Dict[str, Any]:
        """
        Legacy alias for :meth:`get_status`.

        This method exists to preserve the public API of v0.9.x.
        """
        return self.get_status(test_id)