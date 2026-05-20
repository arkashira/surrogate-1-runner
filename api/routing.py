import time
import threading
from typing import Dict, Any, List, Tuple, Callable

from .strategies import ProviderStrategy, ProviderRegistry


# Cache TTL in seconds (e.g., 15 minutes)
CACHE_TTL = 15 * 60


class PricingCache:
    """Simple in-memory cache for provider pricing data."""

    def __init__(self, ttl: int = CACHE_TTL):
        self.ttl = ttl
        self._data: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self._lock = threading.Lock()

    def get(self, provider: str) -> Dict[str, Any]:
        with self._lock:
            entry = self._data.get(provider)
            if entry and (time.time() - entry[0]) < self.ttl:
                return entry[1]
            # Cache miss or stale
            pricing = ProviderRegistry.fetch_pricing(provider)
            self._data[provider] = (time.time(), pricing)
            return pricing

    def invalidate(self, provider: str):
        with self._lock:
            self._data.pop(provider, None)

    def clear(self):
        with self._lock:
            self._data.clear()


class RoutePlanner:
    """Main routing engine selecting the cheapest provider."""

    def __init__(self, providers: List[str], cache: PricingCache | None = None):
        self.providers = providers
        self.cache = cache or PricingCache()

    def _cost_for(self, provider: str, request_params: Dict[str, Any]) -> float:
        pricing = self.cache.get(provider)
        strategy = ProviderRegistry.get_strategy(provider)
        return strategy.cost(pricing, request_params)

    def select_provider(self, request_params: Dict[str, Any]) -> Tuple[str, float]:
        if not self.providers:
            raise ValueError("No providers configured for routing")

        cheapest = None
        cheapest_cost = float("inf")

        for provider in self.providers:
            try:
                cost = self._cost_for(provider, request_params)
                if cost < cheapest_cost:
                    cheapest_cost = cost
                    cheapest = provider
            except Exception:
                # Skip providers that fail to provide a cost
                continue

        if cheapest is None:
            raise ValueError("Unable to determine a cheapest provider")

        return cheapest, cheapest_cost


def route_request(request_params: Dict[str, Any]) -> Dict[str, Any]:
    """Public helper to route request to cheapest provider."""
    planner = RoutePlanner(ProviderRegistry.all_providers())
    provider, cost = planner.select_provider(request_params)
    return {"provider": provider, "cost": cost}