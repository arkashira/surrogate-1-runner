"""Configuration module for tenant-specific feature flags."""
import os
from typing import Dict, Any

# Default configuration with environment override
DEFAULT_FINANCIAL_INSIGHTS_ENABLED = os.getenv('FINANCIAL_INSIGHTS_ENABLED', 'false').lower() == 'true'

# Tenant-specific configuration
TENANT_CONFIG: Dict[str, Dict[str, Any]] = {
    "tenant_a": {
        "name": "Tenant A",
        "FINANCIAL_INSIGHTS_ENABLED": True,
    },
    "tenant_b": {
        "name": "Tenant B",
        "FINANCIAL_INSIGHTS_ENABLED": False,
    },
    # Additional tenants can be added here
}

def get_financial_insights_enabled(tenant_id: str) -> bool:
    """Check if financial insights is enabled for a given tenant.

    Args:
        tenant_id: The unique identifier of the tenant

    Returns:
        bool: True if enabled, False otherwise
    """
    tenant_cfg = TENANT_CONFIG.get(tenant_id, {})
    return tenant_cfg.get("FINANCIAL_INSIGHTS_ENABLED", DEFAULT_FINANCIAL_INSIGHTS_ENABLED)