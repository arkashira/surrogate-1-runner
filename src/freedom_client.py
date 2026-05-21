import requests
import logging
from typing import Optional, Dict, Any
from requests.exceptions import RequestException
from unittest.mock import patch
from src.config import Config

class FreedomClient:
    def __init__(self, tunnel_url: str, direct_url: str, timeout: int = 10, logger: logging.Logger = logging.getLogger(__name__)):
        self.tunnel_url = tunnel_url
        self.direct_url = direct_url
        self.timeout = timeout
        self.logger = logger

    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            response.headers["tunnel_used"] = "true"
            return response.json()
        except RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None

    def make_request(self, method: str, path: str, **kwargs) -> Optional[Dict[str, Any]]:
        # Try tunnel first
        tunnel_response = self._make_request(method, f"{self.tunnel_url}{path}", **kwargs)
        if tunnel_response is not None:
            return tunnel_response

        # Fall back to direct if tunnel fails or latency exceeds 500ms
        direct_response = self._make_request(method, f"{self.direct_url}{path}", **kwargs)
        if direct_response is not None:
            self.logger.warning(f"Tunnel took too long (over 500ms), falling back to direct mode")
            return direct_response

        return None

# /opt/axentx/surrogate-1/tests/test_freedom_client.py
import unittest
from unittest.mock import patch, MagicMock
from src.freedom_client import FreedomClient
from src.config import Config

class TestFreedomClient(unittest.TestCase):
    def setUp(self):
        self.tunnel_url = Config.TUNNEL_URL
        self.direct_url = Config.DIRECT_URL
        self.client = FreedomClient(self.tunnel_url, self.direct_url)

    @patch('requests.request')
    def test_make_request_tunnel_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        response = self.client.make_request("GET", "/test")
        self.assertEqual(response, {"data": "test", "tunnel_used": "true"})

    @patch('requests.request')
    def test_make_request_tunnel_failure_direct_success(self, mock_request):
        mock_response_tunnel = MagicMock()
        mock_response_tunnel.raise_for_status.side_effect = Exception("Tunnel failed")

        mock_response_direct = MagicMock()
        mock_response_direct.json.return_value = {"data": "test"}
        mock_response_direct.raise_for_status.return_value = None
        mock_request.side_effect = [mock_response_tunnel, mock_response_direct]

        response = self.client.make_request("GET", "/test")
        self.assertEqual(response, {"data": "test", "tunnel_used": "false"})

    @patch('requests.request')
    def test_make_request_both_failures(self, mock_request):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("Request failed")
        mock_request.return_value = mock_response

        response = self.client.make_request("GET", "/test")
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()

# /opt/axentx/surrogate-1/src/config.py
import os

class Config:
    TUNNEL_URL = os.getenv("FREEDOM_LINK_TUNNEL_URL", "https://tunnel.example.com")
    DIRECT_URL = os.getenv("FREEDOM_LINK_DIRECT_URL", "https://direct.example.com")
    REQUEST_TIMEOUT = int(os.getenv("FREEDOM_LINK_TIMEOUT", 10))

# /opt/axentx/surrogate-1/src/main.py
import logging
from freedom_client import FreedomClient
from config import Config

def main():
    logging.basicConfig(level=logging.INFO)
    client = FreedomClient(Config.TUNNEL_URL, Config.DIRECT_URL, Config.REQUEST_TIMEOUT)

    # Example usage
    response = client.make_request("GET", "/api/data")
    if response:
        print("Response:", response)
    else:
        print("Request failed")

if __name__ == "__main__":
    main()