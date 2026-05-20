"""Tenant-aware configuration loader with robust error handling and caching."""
from __future__ import annotations
import importlib
import logging
from typing import Any, Dict, Optional
from functools import lru_cache

# Constants
DEFAULT_TENANT_CONFIG: Dict[str, Dict[str, Any]] = {}
CONFIG_MODULE_PATH = "config"  # Relative import path

@lru_cache(maxsize=128)
def _load_global_config() -> Dict[str, Dict[str, Any]]:
    """Load and cache the global tenant configuration with robust error handling."""
    try:
        config_module = importlib.import_module(CONFIG_MODULE_PATH)
        tenant_cfg = getattr(config_module, "TENANT_CONFIG", None)
        if isinstance(tenant_cfg, dict):
            return tenant_cfg
        logging.getLogger(__name__).warning(
            "TENANT_CONFIG is missing or not a dict; using empty config."
        )
    except Exception as exc:
        logging.getLogger(__name__).error(
            "Failed to load global config: %s", exc
        )
    return DEFAULT_TENANT_CONFIG

def get_tenant_config(tenant_id: str) -> Dict[str, Any]:
    """Retrieve configuration for a tenant with fallback to empty dict."""
    return _load_global_config().get(tenant_id, {})

def is_financial_insights_enabled(tenant_id: str) -> bool:
    """Check if financial insights are enabled for a tenant."""
    return bool(get_tenant_config(tenant_id).get("FINANCIAL_INSIGHTS_ENABLED", False))