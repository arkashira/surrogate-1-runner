from typing import Any, Dict
from .llm_response import LLMResponse

class ClaudeProvider:
    """
    Claude LLM provider wrapper that returns a consistent LLMResponse.
    """

    def __init__(self, client: Any, model: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the provider with a client instance and model name.
        
        Args:
            client: An instance of the Anthropic SDK client (e.g., anthropic.Anthropic).
            model: The model identifier to use (default: claude-3-5-sonnet-20240620).
        """
        self.client = client
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 1024, **kwargs) -> LLMResponse:
        """
        Generate text using Claude and wrap the response in LLMResponse.

        Args:
            prompt (str): The prompt to send to Claude.
            max_tokens (int): Maximum number of tokens to generate.
            **kwargs: Additional arguments forwarded to the Claude client (e.g., temperature, top_p).

        Returns:
            LLMResponse: Consistent response object.
        """
        # Call the underlying Claude client
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            **kwargs,
        )

        # Extract text safely using getattr to handle different SDK versions
        text = ""
        if hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            # Handle modern SDK structure (message.content) and legacy structure (content)
            text = getattr(choice, "message", {}).get("content", "")
            if not text:
                text = getattr(choice, "content", "")

        # Extract usage statistics
        usage = {}
        if hasattr(response, "usage"):
            usage = {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
                "completion_tokens": getattr(response.usage, "completion_tokens", None),
                "total_tokens": getattr(response.usage, "total_tokens", None),
            }

        # Extract finish reason
        finish_reason = ""
        if hasattr(response, "choices") and response.choices:
            finish_reason = getattr(response.choices[0], "finish_reason", "")

        return LLMResponse(
            text=text,
            usage=usage,
            finish_reason=finish_reason
        )