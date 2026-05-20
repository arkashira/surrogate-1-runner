"""
Rate‑limiting middleware for LLM providers.

The module provides a simple, async‑compatible token‑bucket implementation
that can be used as a context manager or decorator.  Provider‑specific limits
are defined in ``PROVIDER_RATE_LIMITS`` (calls per *period* seconds).  The
limiter automatically discards timestamps that fall outside the current
window, ensuring that the configured rate is never exceeded.

Typical usage:

    from rate_limiter import rate_limit

    @rate_limit("openai")
    async def call_openai(...):
        ...

or:

    async with get_limiter("anthropic"):
        await provider.generate(...)
"""

import asyncio
import collections
from typing import Dict

# --------------------------------------------------------------------------- #
# Configuration – calls per period (seconds).  Adjust as needed for each
# provider.  The values are deliberately conservative to avoid hitting external
# API limits.
# --------------------------------------------------------------------------- #
PROVIDER_RATE_LIMITS: Dict[str, Dict[str, int]] = {
    # provider_name: {"max_calls": int, "period": int (seconds)}
    "openai": {"max_calls": 60, "period": 60},        # 60 calls per minute
    "anthropic": {"max_calls": 30, "period": 60},    # 30 calls per minute
    "cohere": {"max_calls": 20, "period": 60},       # 20 calls per minute
    # Add additional providers here.
}

# --------------------------------------------------------------------------- #
# Core rate‑limiter implementation.
# --------------------------------------------------------------------------- #
class AsyncRateLimiter:
    """
    Async context manager that enforces a maximum number of calls within a
    sliding time window.

    Example:
        async with limiter:
            await provider.do_something()
    """

    __slots__ = ("_max_calls", "_period", "_timestamps", "_lock")

    def __init__(self, max_calls: int, period: int):
        self._max_calls = max_calls
        self._period = period
        self._timestamps: collections.deque[float] = collections.deque()
        self._lock = asyncio.Lock()

    async def __aenter__(self):
        async with self._lock:
            loop = asyncio.get_event_loop()
            now = loop.time()

            # Remove timestamps that are older than the current window.
            while self._timestamps and self._timestamps[0] <= now - self._period:
                self._timestamps.popleft()

            # If we have exhausted the quota, wait until the oldest entry expires.
            if len(self._timestamps) >= self._max_calls:
                earliest = self._timestamps[0]
                sleep_duration = (earliest + self._period) - now
                await asyncio.sleep(sleep_duration)

            # Record the current call.
            self._timestamps.append(loop.time())

    async def __aexit__(self, exc_type, exc, tb):
        # No cleanup required; timestamps are pruned on entry.
        return False


# --------------------------------------------------------------------------- #
# Singleton registry – one limiter per provider.
# --------------------------------------------------------------------------- #
_limiter_registry: Dict[str, AsyncRateLimiter] = {}


def get_limiter(provider_name: str) -> AsyncRateLimiter:
    """
    Retrieve (or create) a rate limiter for the given provider.

    Parameters
    ----------
    provider_name: str
        The identifier used in ``PROVIDER_RATE_LIMITS``.

    Returns
    -------
    AsyncRateLimiter
        A shared limiter instance.
    """
    if provider_name not in PROVIDER_RATE_LIMITS:
        raise ValueError(f"No rate‑limit configuration for provider '{provider_name}'")

    if provider_name not in _limiter_registry:
        cfg = PROVIDER_RATE_LIMITS[provider_name]
        _limiter_registry[provider_name] = AsyncRateLimiter(
            max_calls=cfg["max_calls"], period=cfg["period"]
        )
    return _limiter_registry[provider_name]


# --------------------------------------------------------------------------- #
# Decorator helper – convenient for wrapping async call functions.
# --------------------------------------------------------------------------- #
def rate_limit(provider_name: str):
    """
    Async decorator that applies the provider‑specific rate limiter.

    Example:
        @rate_limit("openai")
        async def chat_completion(...):
            ...

    The decorated function will automatically wait if the provider's quota
    would be exceeded.
    """
    limiter = get_limiter(provider_name)

    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with limiter:
                return await func(*args, **kwargs)

        return wrapper

    return decorator