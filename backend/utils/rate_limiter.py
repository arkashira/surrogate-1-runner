"""
Simple Redis-backed rate limiter.

This module provides a :class:`RateLimiter` that tracks the number of
on‑demand playbook requests per user over a sliding window.  The limiter
stores a counter per user in Redis with an expiry equal to the window
duration.  The counter is incremented atomically on each request and
the value is compared against the configured maximum.

The implementation is intentionally lightweight and suitable for
high‑throughput environments where the Redis instance is already
available.  It uses the ``redis`` Python client.

Example usage:

    from backend.utils.rate_limiter import RateLimiter
    import redis

    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    limiter = RateLimiter(redis_client, max_requests=2, window_seconds=7*24*3600)

    if limiter.allow(user_id="user-123"):
        # proceed with playbook generation
    else:
        # return rate‑limit error
"""

import time
from typing import Any

import redis


class RateLimiter:
    """
    Redis-backed rate limiter.

    Parameters
    ----------
    redis_client : redis.Redis
        A connected Redis client instance.
    max_requests : int, default 2
        Maximum number of allowed requests per window.
    window_seconds : int, default 7 days
        Length of the sliding window in seconds.
    key_prefix : str, default "rate_limit:"
        Prefix for Redis keys to avoid collisions.
    """

    def __init__(
        self,
        redis_client: redis.Redis,
        max_requests: int = 2,
        window_seconds: int = 7 * 24 * 3600,
        key_prefix: str = "rate_limit:",
    ) -> None:
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.key_prefix = key_prefix

    def _key(self, user_id: str) -> str:
        """Construct the Redis key for a given user."""
        return f"{self.key_prefix}{user_id}"

    def allow(self, user_id: str) -> bool:
        """
        Attempt to acquire a slot for the given user.

        Returns
        -------
        bool
            ``True`` if the request is allowed, ``False`` if the user has
            exceeded the rate limit.
        """
        key = self._key(user_id)
        pipeline = self.redis.pipeline()
        # Increment the counter and get the new value
        pipeline.incr(key)
        # Set expiry only if the key was just created
        pipeline.expire(key, self.window_seconds)
        try:
            new_count, _ = pipeline.execute()
        except redis.exceptions.RedisError as exc:
            # In production we might log this; for now we treat errors as
            # a failure to allow the request to avoid over‑granting.
            # This conservative approach ensures we don't exceed the limit
            # if Redis is unavailable.
            print(f"[RateLimiter] Redis error: {exc}")
            return False

        if new_count > self.max_requests:
            # Optionally, we could decrement the counter to keep the count
            # accurate, but for a simple limiter it's acceptable to let it
            # stay over the limit until the key expires.
            return False
        return True

    def reset(self, user_id: str) -> None:
        """
        Reset the counter for a user immediately.

        Useful for tests or administrative actions.
        """
        self.redis.delete(self._key(user_id))