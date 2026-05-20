"""
Public SDK for surrogate-1.

Exposes a single `generate` function that delegates to the appropriate LLM provider.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from surrogate1.providers.factory import ProviderFactory, ProviderNotSupportedError


@dataclass
class LLMResponse:
    """
    Common response schema for all providers.

    Attributes
    ----------
    text : str
        The generated text.
    usage : Dict[str, Any]
        Token usage statistics (e.g., prompt_tokens, completion_tokens, total_tokens).
    finish_reason : str
        Reason the generation finished (e.g., 'stop', 'length', 'error').
    """
    text: str
    usage: Dict[str, Any]
    finish_reason: str


def generate(prompt: str, provider: str, **kwargs) -> LLMResponse:
    """
    Generate text using the specified LLM provider.

    Parameters
    ----------
    prompt : str
        The input prompt for the LLM.
    provider : str
        Identifier of the provider ('claude', 'minimax', 'openai').
    **kwargs
        Additional keyword arguments forwarded to the provider's 
        constructor and generate method.

    Returns
    -------
    LLMResponse
        Normalized response object.

    Raises
    ------
    ProviderNotSupportedError
        If the provider is not supported.
    """
    provider_instance = ProviderFactory.get_provider(provider, **kwargs)
    
    # Each provider must implement generate() returning dict with
    # 'text', 'usage', 'finish_reason' keys
    provider_response = provider_instance.generate(prompt, **kwargs)
    
    return LLMResponse(
        text=provider_response.get("text", ""),
        usage=provider_response.get("usage", {}),
        finish_reason=provider_response.get("finish_reason", ""),
    )


__all__ = ["generate", "LLMResponse", "ProviderNotSupportedError"]