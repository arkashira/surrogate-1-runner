from typing import Dict, Any
from .llm_interface import LLMInterface
import anthropic

class AnthropicIntegration(LLMInterface):
    """Concrete implementation of LLMInterface for Anthropic."""

    def __init__(self):
        self.api_key = None
        self.model = None

    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the Anthropic integration.

        Args:
            config: A dictionary containing 'api_key' and 'model' keys.
        """
        self.api_key = config.get('api_key')
        self.model = config.get('model')
        anthropic.api_key = self.api_key

    def generate_response(self, prompt: str, system_message: str = None, **kwargs) -> str:
        """Generate a response from Anthropic's LLM.

        Args:
            prompt: The input prompt for the LLM.
            system_message: Optional system message to guide the LLM's behavior.
            **kwargs: Additional arguments specific to Anthropic's API.

        Returns:
            The generated response from Anthropic's LLM.
        """
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.completions.create(
            model=self.model,
            prompt=prompt,
            system=system_message,
            **kwargs
        )
        return response.completion