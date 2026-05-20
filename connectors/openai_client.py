import os
from typing import Generator, Dict, Any, Optional
import openai

class OpenAIClient:
    """Enhanced OpenAI client with standardized responses, usage tracking, and streaming support."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not set. Provide via OPENAI_API_KEY env var.")
        openai.api_key = self.api_key
        self.model = model
        self._usage_metrics = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def _standardize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize response format across all methods."""
        usage = response.get("usage", {})
        self._update_usage_metrics(usage)

        content = ""
        if response.get("choices"):
            first_choice = response["choices"][0]
            message = first_choice.get("message", {}) if "message" in first_choice else first_choice
            content = message.get("content", "")

        return {
            "content": content,
            "usage": usage,
            "model": response.get("model"),
            "provider": "openai",
            "metadata": response.get("metadata", {}),
        }

    def _update_usage_metrics(self, usage: Dict[str, int]) -> None:
        """Update internal usage metrics."""
        self._usage_metrics["prompt_tokens"] += usage.get("prompt_tokens", 0)
        self._usage_metrics["completion_tokens"] += usage.get("completion_tokens", 0)
        self._usage_metrics["total_tokens"] += usage.get("total_tokens", 0)

    def chat_completion(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Dict[str, Any]:
        """Synchronous chat completion with standardized response."""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
        )
        return self._standardize_response(response)

    def chat_completion_stream(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Generator[str, None, None]:
        """Streaming chat completion with incremental content and final usage metrics."""
        stream = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        for chunk in stream:
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    yield content

        # After stream ends, update metrics if available
        if hasattr(stream, "usage"):
            self._update_usage_metrics(stream.usage)

    def get_usage_metrics(self) -> Dict[str, int]:
        """Return accumulated usage metrics."""
        return self._usage_metrics

# Example usage
if __name__ == "__main__":
    client = OpenAIClient()

    # Synchronous completion
    response = client.chat_completion([{"role": "user", "content": "Hello, how are you?"}])
    print(response["content"])

    # Streaming completion
    print("\nStreaming response:")
    for chunk in client.chat_completion_stream([{"role": "user", "content": "Tell me a story"}]):
        print(chunk, end="", flush=True)

    # Usage metrics
    print("\n\nUsage metrics:", client.get_usage_metrics())