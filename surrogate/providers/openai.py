import os
import openai  # pip install openai
from typing import Any
from .base import BaseProvider, ProviderError

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str | None = None, **options: Any):
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ProviderError("OpenAI API key missing", code="NO_API_KEY")
        openai.api_key = self._api_key
        self.configure(**options)

    @property
    def name(self) -> str:
        return "OpenAI"

    def generate(self, prompt: str, **kwargs: Any) -> str:
        try:
            resp = openai.ChatCompletion.create(
                model=kwargs.get("model", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 256),
            )
            return resp.choices[0].message["content"].strip()
        except openai.error.OpenAIError as exc:          # pragma: no‑cover
            raise ProviderError(str(exc), code=getattr(exc, "code", None))