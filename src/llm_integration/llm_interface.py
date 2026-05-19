from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMInterface(ABC):
    """Abstract base class for LLM integrations."""

    @abstractmethod
    def generate_response(self, prompt: str, system_message: str = None, **kwargs) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The input prompt for the LLM.
            system_message: Optional system message to guide the LLM's behavior.
            **kwargs: Additional arguments specific to the LLM provider.

        Returns:
            The generated response from the LLM.
        """
        pass

    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the LLM integration with provider-specific settings.

        Args:
            config: A dictionary containing configuration parameters.
        """
        pass