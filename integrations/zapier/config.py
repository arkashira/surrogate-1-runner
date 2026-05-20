"""
Zapier configuration using environment variables.

Supports both simple webhook-only mode and full REST API mode.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ZapierConfig:
    """Configuration for Zapier integration."""
    
    # Webhook mode (simple)
    webhook_url: Optional[str] = field(
        default=None,
        default_factory=lambda: os.environ.get("ZAPIER_WEBHOOK_URL")
    )
    
    # REST API mode (advanced)
    api_key: Optional[str] = field(
        default=None,
        default_factory=lambda: os.environ.get("ZAPIER_API_KEY")
    )
    client_id: Optional[str] = field(
        default=None,
        default_factory=lambda: os.environ.get("ZAPIER_CLIENT_ID")
    )
    client_secret: Optional[str] = field(
        default=None,
        default_factory=lambda: os.environ.get("ZAPIER_CLIENT_SECRET")
    )
    webhook_secret: Optional[str] = field(
        default=None,
        default_factory=lambda: os.environ.get("ZAPIER_WEBHOOK_SECRET")
    )
    
    # Request settings
    timeout: int = field(default=10)
    verify_ssl: bool = field(default=True)
    
    @property
    def is_configured(self) -> bool:
        """Check if at least one integration method is configured."""
        return bool(self.webhook_url or self.api_key)
    
    @property
    def mode(self) -> str:
        """Determine which integration mode to use."""
        if self.webhook_url:
            return "webhook"
        if self.api_key:
            return "rest_api"
        return "unconfigured"