from typing import Dict, Any
from .llm_interface import LLMInterface
from .openai_integration import OpenAIIntegration
from .anthropic_integration import AnthropicIntegration

class LLMFactory:
    """Factory class for creating LLM integrations."""

    @staticmethod
    def create_llm(provider: str) -> LLMInterface:
        """Create an instance of the specified LLM provider.

        Args:
            provider: The name of the LLM provider ('openai' or 'anthropic').

        Returns:
            An instance of the specified LLM provider.

        Raises:
            ValueError: If the provider is not supported.
        """
        if provider.lower() == 'openai':
            return OpenAIIntegration()
        elif provider.lower() == 'anthropic':
            return AnthropicIntegration()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")