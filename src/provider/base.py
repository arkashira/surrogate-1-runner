"""Abstract base provider interface for LLM providers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..response import LLMResponse
from ..exceptions import AuthenticationError


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    provider_name: str = ""

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """Generate a response from the LLM.

        Args:
            prompt: The input prompt to send to the LLM.
            **kwargs: Additional provider‑specific parameters.

        Returns:
            LLMResponse: A response object conforming to the common schema.
        """
        ...

    def validate_api_key(self) -> None:
        """Validate that the required API key is present.

        Raises:
            AuthenticationError: If the API key is missing or invalid.
        """
        raise AuthenticationError(
            f"{self.provider_name} provider requires a valid API key."
        )