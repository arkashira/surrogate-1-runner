"""
Provider factory for resolving LLM provider strings to concrete provider classes.
"""

from __future__ import annotations

from typing import Any, Dict, Type

from surrogate1.providers.base_provider import BaseProvider
from surrogate1.providers.claude_provider import ClaudeProvider
from surrogate1.providers.minimax_provider import MinimaxProvider
from surrogate1.providers.openai_provider import OpenAIProvider


class ProviderNotSupportedError(RuntimeError):
    """Raised when an unsupported provider string is requested."""
    
    def __init__(self, provider_name: str, supported: list[str]):
        self.provider_name = provider_name
        self.supported = supported
        super().__init__(
            f"Provider '{provider_name}' is not supported. "
            f"Supported providers: {supported}"
        )


class ProviderFactory:
    """
    Factory that maps provider names to provider classes.
    
    Supported providers:
        - 'claude'   -> ClaudeProvider
        - 'minimax' -> MinimaxProvider
        - 'openai'  -> OpenAIProvider
    """
    
    _PROVIDER_MAP: Dict[str, Type[BaseProvider]] = {
        "claude": ClaudeProvider,
        "minimax": MinimaxProvider,
        "openai": OpenAIProvider,
    }

    @classmethod
    def get_provider(cls, provider_name: str, **kwargs) -> BaseProvider:
        """
        Return an instance of the provider class corresponding to `provider_name`.

        Parameters
        ----------
        provider_name : str
            The provider identifier (case-insensitive).
        **kwargs
            Arguments forwarded to the provider constructor.

        Returns
        -------
        BaseProvider
            An instance of the requested provider.

        Raises
        ------
        ProviderNotSupportedError
            If the provider is not in the supported list.
        """
        key = provider_name.lower()
        provider_class = cls._PROVIDER_MAP.get(key)
        
        if provider_class is None:
            raise ProviderNotSupportedError(
                provider_name, 
                list(cls._PROVIDER_MAP.keys())
            )
        
        return provider_class(**kwargs)

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseProvider]) -> None:
        """
        Register a new provider dynamically.
        
        Parameters
        ----------
        name : str
            Provider identifier (will be lowercased).
        provider_class : Type[BaseProvider]
            Provider class to register.
        """
        cls._PROVIDER_MAP[name.lower()] = provider_class

    @classmethod
    def supported_providers(cls) -> list[str]:
        """Return list of supported provider names."""
        return list(cls._PROVIDER_MAP.keys())