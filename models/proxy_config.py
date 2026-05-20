class ProxyConfig:
    def __init__(self, ai_endpoints, proxy_url):
        self.ai_endpoints = ai_endpoints
        self.proxy_url = proxy_url

    def to_dict(self):
        return {
            "ai_endpoints": self.ai_endpoints,
            "proxy_url": self.proxy_url
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["ai_endpoints"], data["proxy_url"])

# /opt/axentx/surrogate-1/schemas/proxy_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Proxy Configuration",
  "type": "object",
  "properties": {
    "ai_endpoints": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "proxy_url": {
      "type": "string"
    }
  },
  "required": [
    "ai_endpoints",
    "proxy_url"
  ]
}

# /opt/axentx/surrogate-1/ui/proxy_config.py
from flask import Flask, request, jsonify
from .models import ProxyConfig

app = Flask(__name__)

@app.route("/proxy_config", methods=["POST"])
def create_proxy_config():
    data = request.get_json()
    proxy_config = ProxyConfig.from_dict(data)
    return jsonify(proxy_config.to_dict())

# /opt/axentx/surrogate-1/ui/tests/test_proxy_config.py
import unittest
from unittest.mock import Mock
from .proxy_config import app

class TestProxyConfigAPI(unittest.TestCase):
    def test_create_proxy_config(self):
        with app.test_client() as client:
            data = {
                "ai_endpoints": ["https://claudex.com", "https://gpt-4.com"],
                "proxy_url": "https://my-proxy.com"
            }
            response = client.post("/proxy_config", json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                "ai_endpoints": ["https://claudex.com", "https://gpt-4.com"],
                "proxy_url": "https://my-proxy.com"
            })

if __name__ == "__main__":
    unittest.main()

## Summary
- Implemented ProxyConfig model in models/proxy_config.py
- Defined proxy schema in schemas/proxy_schema.json
- Created API endpoint to create proxy config in ui/proxy_config.py
- Added unit test for proxy config API in ui/tests/test_proxy_config.py