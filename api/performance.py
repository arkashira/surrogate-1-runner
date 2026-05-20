"""
Performance monitoring and provider selection module.

Provides a simple in-memory cache of provider performance metrics and
functions to update and retrieve the best provider for a given request
parameter set.
"""

import time
import threading
from typing import Dict, Tuple, List, Any, Optional
import requests
import cachetools

# Configuration
PERFORMANCE_ENDPOINTS = {
    "provider_a": "https://api.provider_a.com/performance",
    "provider_b": "https://api.provider_b.com/performance",
    "provider_c": "https://api.provider_c.com/performance",
}
CACHE_TTL_SECONDS = 300  # 5 minutes
MAX_CACHE_SIZE = 10

# In-memory cache structure:
# {
#     "provider_a": {"timestamp": 1234567890, "metrics": {...}},
#     ...
# }
_performance_cache = cachetools.TTLCache(maxsize=MAX_CACHE_SIZE, ttl=CACHE_TTL_SECONDS)
_cache_lock = threading.Lock()

def _fetch_performance(provider: str) -> Optional[Dict[str, Any]]:
    """
    Fetch performance metrics from the provider's monitoring endpoint.
    Returns a dict of metrics or None if the request fails.
    """
    url = PERFORMANCE_ENDPOINTS.get(provider)
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

def update_cache() -> None:
    """
    Refresh the performance cache for all providers.
    This function can be scheduled to run periodically.
    """
    global _performance_cache
    new_cache: Dict[str, Dict[str, Any]] = {}
    now = time.time()
    for provider in PERFORMANCE_ENDPOINTS:
        metrics = _fetch_performance(provider)
        if metrics is not None:
            new_cache[provider] = {"timestamp": now, "metrics": metrics}
    with _cache_lock:
        _performance_cache.update(new_cache)

def get_best_provider(request_params: Dict[str, Any]) -> Optional[str]:
    """
    Return the provider with the best (lowest) average latency for the given
    request parameters. If no data is available, returns None.
    """
    with _cache_lock:
        if not _performance_cache:
            return None
        best_provider = None
        best_latency = float("inf")
        for provider, data in _performance_cache.items():
            metrics = data["metrics"]
            # Assume metrics contain 'average_latency_ms' field
            latency = metrics.get("average_latency_ms")
            if latency is None:
                continue
            # Optionally adjust based on request_params (e.g., payload size)
            # For now, we just use raw latency.
            if latency < best_latency:
                best_latency = latency
                best_provider = provider
        return best_provider

def get_cached_metrics(provider: str) -> Optional[Dict[str, Any]]:
    """
    Return cached metrics for a provider if still fresh, else None.
    """
    return _performance_cache.get(provider, None)