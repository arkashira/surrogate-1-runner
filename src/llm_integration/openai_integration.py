from typing import Dict, Any
from .llm_interface import LLMInterface
import openai

class OpenAIIntegration(LLMInterface):
    """Concrete implementation of LLMInterface for OpenAI."""

    def __init__(self):
        self.api_key = None
        self.model = None

    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the OpenAI integration.

        Args:
            config: A dictionary containing 'api_key' and 'model' keys.
        """
        self.api_key = config.get('api_key')
        self.model = config.get('model')
        openai.api_key = self.api_key

    def generate_response(self, prompt: str, system_message: str = None, **kwargs) -> str:
        """Generate a response from OpenAI's LLM.

        Args:
            prompt: The input prompt for the LLM.
            system_message: Optional system message to guide the LLM's behavior.
            **kwargs: Additional arguments specific to OpenAI's API.

        Returns:
            The generated response from OpenAI's LLM.
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message['content']