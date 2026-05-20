"""Custom exceptions for Zapier integration."""


class ZapierIntegrationError(Exception):
    """Base exception for Zapier integration failures."""
    pass


class ZapierConfigurationError(ZapierIntegrationError):
    """Raised when Zapier is not properly configured."""
    pass


class ZapierWebhookError(ZapierIntegrationError):
    """Raised when webhook trigger fails."""
    pass


class ZapierAPIError(ZapierIntegrationError):
    """Raised when REST API call fails."""
    pass