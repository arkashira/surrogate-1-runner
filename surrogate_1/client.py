import os
import json
import ssl
import urllib.request
import urllib.error
from typing import Dict, Any

class LLMClient:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.providers = {
            'openai': OpenAIClient(),
            'anthropic': AnthropicClient()
        }
        self.model = model

    def generate_text(self, prompt: str, **kwargs) -> str:
        provider_name = self._get_provider_name(self.model)
        if provider_name not in self.providers:
            raise ValueError(f"Unsupported model: {self.model}")
        return self.providers[provider_name].generate_text(prompt, self.model, **kwargs)

    def _get_provider_name(self, model_name: str) -> str:
        if model_name in MODEL_PROVIDER_MAP:
            return MODEL_PROVIDER_MAP[model_name]
        elif model_name.startswith('gpt'):
            return 'openai'
        elif model_name.startswith('claude'):
            return 'anthropic'
        else:
            raise ValueError(f"Unknown provider for model: {model_name}")


class OpenAIClient:
    def generate_text(self, prompt: str, model: str, **kwargs) -> str:
        endpoint = PROVIDER_ENDPOINTS['openai']
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = self._build_request(prompt, model, **kwargs)
        response = self._make_request(endpoint, headers, payload)
        return response["choices"][0]["message"]["content"]

    def _build_request(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7),
        }
        return payload

    def _make_request(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        
        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method="POST"
        )
        
        ctx = ssl.create_default_context()
        
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                response_body = response.read().decode("utf-8")
                return json.loads(response_body)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(
                f"HTTP {e.code} {e.reason}: {error_body}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Request failed: {e.reason}") from e


class AnthropicClient:
    def generate_text(self, prompt: str, model: str, **kwargs) -> str:
        endpoint = PROVIDER_ENDPOINTS['anthropic']
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
        payload = self._build_request(prompt, model, **kwargs)
        response = self._make_request(endpoint, headers, payload)
        return response["content"][0]["text"]

    def _build_request(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1024),
        }
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        return payload

    def _make_request(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        
        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method="POST"
        )
        
        ctx = ssl.create_default_context()
        
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                response_body = response.read().decode("utf-8")
                return json.loads(response_body)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(
                f"HTTP {e.code} {e.reason}: {error_body}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Request failed: {e.reason}") from e


PROVIDER_ENDPOINTS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
}

MODEL_PROVIDER_MAP = {
    # OpenAI models
    "gpt-3.5-turbo": "openai",
    "gpt-3.5": "openai",
    "gpt-4": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4o": "openai",
    # Anthropic models
    "claude-3-haiku-20240307": "anthropic",
    "claude-3-sonnet-20240229": "anthropic",
    "claude-3-opus-20240229": "anthropic",
    "claude-3-5-sonnet-20240620": "anthropic",
}