import requests
import logging
from typing import Dict, Any
from datetime import datetime
import json
import os

class ClaudeAPI:
    def __init__(self, api_key: str, base_url: str = "https://api.claude.ai"):
        self.api_key = api_key
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.audit_log_path = "/var/log/axentx/claude_audit.log"

    def _log_access(self, endpoint: str, request_data: Dict[str, Any], response: Dict[str, Any]):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "request": request_data,
            "response": response
        }
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def complete_prompt(self, prompt: str, max_tokens: int = 100) -> str:
        endpoint = "v1/completions"
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        try:
            response = self._make_request(endpoint, payload)
            self._log_access(endpoint, payload, response)
            return response["choices"][0]["text"]
        except Exception as e:
            self.logger.error(f"Error completing prompt: {e}")
            raise

    def analyze_text(self, text: str) -> Dict[str, Any]:
        endpoint = "v1/analyze"
        payload = {
            "text": text
        }
        try:
            response = self._make_request(endpoint, payload)
            self._log_access(endpoint, payload, response)
            return response
        except Exception as e:
            self.logger.error(f"Error analyzing text: {e}")
            raise

    def get_usage_stats(self) -> Dict[str, Any]:
        endpoint = "v1/usage"
        try:
            response = self._make_request(endpoint, {})
            self._log_access(endpoint, {}, response)
            return response
        except Exception as e:
            self.logger.error(f"Error getting usage stats: {e}")
            raise