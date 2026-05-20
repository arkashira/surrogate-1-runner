"""
Provider routing module.

Uses performance monitoring data to route API requests to the best provider.
"""

from typing import Dict, Any, Optional
from .performance import get_best_provider, get_cached_metrics

# Example mapping of provider names to their API endpoints
PROVIDER_ENDPOINTS = {
    "provider_a": "https://api.provider_a.com/v1",
    "provider_b": "https://api.provider_b.com/v1",
    "provider_c": "https://api.provider_c.com/v1",
}

def route_request(request_params: Dict[str, Any]) -> Optional[str]:
    """
    Determine the best provider for the given request parameters and
    return its base URL. Returns None if no provider is available.
    """
    best_provider = get_best_provider(request_params)
    if not best_provider:
        return None
    return PROVIDER_ENDPOINTS.get(best_provider)

def get_provider_metrics(provider_name: str) -> Optional[Dict[str, Any]]:
    """
    Expose cached metrics for a specific provider.
    """
    return get_cached_metrics(provider_name)