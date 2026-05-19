import requests
from typing import Any, Dict, List, Union

class Client:
    """
    Thin wrapper around the HTTP client used by the SDK.
    Keeps a single `requests.Session` so that keep‑alive and
    connection pooling are handled automatically.
    """

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def get(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Perform a GET request and return the decoded JSON payload.
        Raises `requests.HTTPError` if the status code is 4xx/5xx.
        """
        url = f"{self.base_url}{endpoint}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()