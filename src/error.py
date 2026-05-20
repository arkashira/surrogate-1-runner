from typing import Optional
from enum import Enum


class ErrorCode(Enum):
    """Standardized error codes across all LLM providers."""
    INVALID_REQUEST = "INVALID_REQUEST"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    TIMEOUT = "TIMEOUT"
    CONTENT_FILTERED = "CONTENT_FILTERED"
    UNKNOWN = "UNKNOWN"


class LLMError(Exception):
    """Standardized exception for all LLM provider errors."""
    
    def __init__(
        self, 
        code: ErrorCode | str, 
        message: str, 
        provider: str,
        retryable: bool = False,
        original_error: Optional[Exception] = None
    ):
        self.code = code if isinstance(code, str) else code.value
        self.message = message
        self.provider = provider
        self.retryable = retryable
        self.original_error = original_error
        
        super().__init__(f"{provider}: {self.code} - {message}")
    
    def __str__(self):
        return f"{self.provider}: {self.code} - {self.message}"
    
    def __repr__(self):
        return f"LLMError(code={self.code!r}, message={self.message!r}, provider={self.provider!r}, retryable={self.retryable})"
    
    @property
    def is_retryable(self) -> bool:
        """Check if the error is transient and worth retrying."""
        return self.retryable or self.code in (
            ErrorCode.RATE_LIMIT_EXCEEDED.value,
            ErrorCode.SERVICE_UNAVAILABLE.value,
            ErrorCode.TIMEOUT.value,
        )