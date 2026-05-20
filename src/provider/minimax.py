"""
Minimax LLM Provider Implementation

Provides a consistent interface for interacting with Minimax's LLM API,
returning structured responses that integrate seamlessly with the broader
provider ecosystem.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from enum import Enum
import json
import hashlib
import time


class FinishReason(Enum):
    """Enumeration of possible completion finish reasons."""
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    ERROR = "error"


@dataclass
class Usage:
    """Token usage statistics for an LLM response."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens
        }


@dataclass 
class LLMResponse:
    """
    Structured response from an LLM provider.
    
    This dataclass provides a consistent response format across all providers,
    making it easy to switch between different LLM backends without changing
    consumer code.
    """
    text: str
    usage: Usage
    finish_reason: str
    model: str = ""
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert response to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation suitable for JSON encoding.
        """
        return {
            "text": self.text,
            "usage": self.usage.to_dict() if isinstance(self.usage, Usage) else self.usage,
            "finish_reason": self.finish_reason,
            "model": self.model,
            "request_id": self.request_id,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Serialize response to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @property
    def is_success(self) -> bool:
        """Check if the response represents a successful completion."""
        return self.finish_reason == FinishReason.STOP.value


class MinimaxError(Exception):
    """Base exception for Minimax provider errors."""
    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.code = code


class APIError(MinimaxError):
    """Raised when the API returns an error response."""
    pass


class RateLimitError(MinimaxError):
    """Raised when rate limits are exceeded."""
    pass


class MinimaxProvider:
    """
    Provider for Minimax LLM API.
    
    This implementation provides a mock interface for development and testing.
    In production, replace the mock implementation with actual API calls.
    
    Attributes:
        api_key: Authentication key for the Minimax API.
        model: Model identifier to use for generation.
        base_url: Optional custom API endpoint URL.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retry attempts for failed requests.
    """
    
    # Default API configuration
    DEFAULT_BASE_URL = "https://api.minimax.chat/v1"
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    
    # Supported models
    SUPPORTED_MODELS = [
        "abab5.5-chat",
        "abab5.5s-chat", 
        "abab6-chat",
        "abab6.5s-chat"
    ]
    
    def __init__(
        self,
        api_key: str,
        model: str = "abab5.5-chat",
        base_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES
    ):
        """
        Initialize the Minimax provider.
        
        Args:
            api_key: Minimax API key for authentication.
            model: Model identifier (default: abab5.5-chat).
            base_url: Custom API endpoint (optional).
            timeout: Request timeout in seconds (default: 30).
            max_retries: Maximum retry attempts (default: 3).
            
        Raises:
            ValueError: If API key is empty or model is unsupported.
        """
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")
        
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model: {model}. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )
        
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
    
    def _generate_request_id(self, prompt: str) -> str:
        """Generate a unique request ID from prompt and timestamp."""
        content = f"{prompt}:{time.time()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for input text.
        
        This is a rough approximation. In production, use tiktoken
        or the API's actual token counting.
        
        Args:
            text: Input text to count tokens for.
            
        Returns:
            Estimated token count.
        """
        # Rough estimate: ~4 characters per token on average
        return max(1, len(text) // 4)
    
    def _mock_generate(self, prompt: str) -> LLMResponse:
        """
        Mock implementation for development and testing.
        
        In production, replace this with actual API call: