"""Custom exceptions for the surrogate‑1 SDK."""

class Surrogate1Error(Exception):
    """Base exception for surrogate‑1 SDK errors."""
    pass


class ProviderNotSupportedError(Surrogate1Error):
    """Raised when an unsupported LLM provider is specified."""

    def __init__(self, provider: str, supported_providers: list[str]):
        self.provider = provider
        self.supported_providers = supported_providers
        super().__init__(
            f"Provider '{provider}' is not supported. "
            f"Supported providers: {', '.join(supported_providers)}"
        )


class APIError(Surrogate1Error):
    """Raised when the LLM provider API returns an error."""

    def __init__(self, message: str, provider: str, status_code: int | None = None):
        self.message = message
        self.provider = provider
        self.status_code = status_code
        super().__init__(f"[{provider}] {message}")


class AuthenticationError(Surrogate1Error):
    """Raised when authentication with the LLM provider fails."""
    pass