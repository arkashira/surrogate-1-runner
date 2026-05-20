"""Standard error object for all LLM providers with comprehensive error mapping."""

from dataclasses import dataclass, field
from typing import Optional, Dict, ClassVar

class ErrorCode:
    """Standardized error codes for LLM providers."""
    # Network errors
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    CONNECTION_FAILED = "connection_failed"

    # Authentication errors
    AUTHENTICATION_ERROR = "authentication_error"
    INVALID_API_KEY = "invalid_api_key"
    PERMISSION_DENIED = "permission_denied"

    # Rate limiting
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    QUOTA_EXCEEDED = "quota_exceeded"

    # Provider-specific errors
    PROVIDER_ERROR = "provider_error"
    INVALID_REQUEST = "invalid_request"
    MODEL_NOT_FOUND = "model_not_found"
    CONTENT_FILTERED = "content_filtered"

    # Unknown errors
    UNKNOWN_ERROR = "unknown_error"

    ERROR_CODE_MEANINGS: ClassVar[Dict[str, str]] = {
        NETWORK_ERROR: "Network connectivity issue or DNS failure",
        TIMEOUT: "Request timed out waiting for response",
        CONNECTION_FAILED: "Failed to establish connection to provider",
        AUTHENTICATION_ERROR: "General authentication failure",
        INVALID_API_KEY: "API key is invalid, expired, or revoked",
        PERMISSION_DENIED: "Insufficient permissions for the requested operation",
        RATE_LIMIT_EXCEEDED: "Too many requests, retry after cooldown",
        QUOTA_EXCEEDED: "Monthly or daily usage quota exceeded",
        PROVIDER_ERROR: "Provider returned an unexpected error",
        INVALID_REQUEST: "Request parameters are invalid or malformed",
        MODEL_NOT_FOUND: "Specified model does not exist or is unavailable",
        CONTENT_FILTERED: "Content was filtered due to policy violation",
        UNKNOWN_ERROR: "An unexpected error occurred",
    }

@dataclass
class LLMError(Exception):
    """Standard error object for all LLM providers.

    Attributes:
        code: Error code identifying the type of error
        message: Human-readable error message
        provider: Name of the provider that raised the error
        original_error: Optional original exception that was mapped
    """
    code: str
    message: str
    provider: str
    original_error: Optional[Exception] = field(default=None, repr=False)

    def __post_init__(self):
        if self.code not in ErrorCode.ERROR_CODE_MEANINGS:
            raise ValueError(f"Invalid error code '{self.code}'. Must be one of {list(ErrorCode.ERROR_CODE_MEANINGS.keys())}")

    def __str__(self) -> str:
        return f"[{self.provider}] {self.code}: {self.message}"

def map_provider_error(error: Exception, provider: str, default_code: str = ErrorCode.UNKNOWN_ERROR) -> LLMError:
    """Map a provider-specific error to LLMError.

    Args:
        error: The original exception from the provider
        provider: Name of the provider
        default_code: Fallback error code if mapping fails

    Returns:
        LLMError with appropriate code, message, and provider
    """
    error_message = str(error)
    error_type = type(error).__name__.lower()

    # Map common error patterns
    if "authentication" in error_type or "auth" in error_message.lower():
        code = ErrorCode.AUTHENTICATION_ERROR
    elif "api key" in error_message.lower() or "invalid key" in error_message.lower():
        code = ErrorCode.INVALID_API_KEY
    elif "rate limit" in error_message.lower() or "too many requests" in error_message.lower():
        code = ErrorCode.RATE_LIMIT_EXCEEDED
    elif "quota" in error_message.lower():
        code = ErrorCode.QUOTA_EXCEEDED
    elif "timeout" in error_type or "timed out" in error_message.lower():
        code = ErrorCode.TIMEOUT
    elif "connection" in error_type or "connect" in error_message.lower():
        code = ErrorCode.CONNECTION_FAILED
    elif "network" in error_type:
        code = ErrorCode.NETWORK_ERROR
    elif "permission" in error_message.lower() or "forbidden" in error_type:
        code = ErrorCode.PERMISSION_DENIED
    elif "not found" in error_message.lower() or "model" in error_message.lower():
        code = ErrorCode.MODEL_NOT_FOUND
    elif "invalid request" in error_message.lower() or "bad request" in error_type:
        code = ErrorCode.INVALID_REQUEST
    else:
        code = default_code

    return LLMError(
        code=code,
        message=error_message,
        provider=provider,
        original_error=error
    )

# src/__init__.py
"""Public interface for the surrogate-1 package."""

from .errors import LLMError, ErrorCode, map_provider_error

__all__ = ["LLMError", "ErrorCode", "map_provider_error"]