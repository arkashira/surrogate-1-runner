import os
import uuid
from typing import Optional

import redis

# ----------------------------------------------------------------------
# Redis client (singleton)
# ----------------------------------------------------------------------
_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# decode_responses=True → we always work with str, not bytes
_redis_client = redis.StrictRedis.from_url(_REDIS_URL, decode_responses=True)

# TTL = 24 h (seconds)
_TTL_SECONDS = 24 * 60 * 60
_KEY_PREFIX = "correlation:"


# ----------------------------------------------------------------------
# Helper – UUID validation
# ----------------------------------------------------------------------
def _validate_uuid4(correlation_id: str) -> uuid.UUID:
    """
    Validate that *correlation_id* is a proper UUID‑v4 string.
    Raises ValueError if the string is not a valid UUID‑v4.
    """
    try:
        uid = uuid.UUID(correlation_id, version=4)
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"'{correlation_id}' is not a valid UUID4") from exc

    # uuid.UUID will accept any version; enforce v4 explicitly
    if uid.version != 4:
        raise ValueError(f"'{correlation_id}' is not a UUID4 (found version {uid.version})")
    return uid


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def store_correlation_id(correlation_id: str) -> None:
    """
    Persist a correlation ID in Redis with a 24‑hour TTL.

    Args:
        correlation_id: UUID4 string.

    Raises:
        ValueError: if *correlation_id* is not a valid UUID4.
        redis.RedisError: any connectivity problem bubbles up.
    """
    _validate_uuid4(correlation_id)
    key = f"{_KEY_PREFIX}{correlation_id}"
    # A dummy value is enough – existence of the key is the signal.
    _redis_client.setex(name=key, time=_TTL_SECONDS, value="1")


def get_correlation_id(correlation_id: str) -> Optional[bool]:
    """
    Check whether a correlation ID exists and has not expired.

    Returns:
        True  – if the key exists,
        None  – otherwise.

    Raises:
        ValueError: if *correlation_id* is not a valid UUID4.
    """
    _validate_uuid4(correlation_id)
    key = f"{_KEY_PREFIX}{correlation_id}"
    return True if _redis_client.get(key) is not None else None


def delete_correlation_id(correlation_id: str) -> None:
    """
    Remove a correlation ID from Redis.

    Raises:
        ValueError: if *correlation_id* is not a valid UUID4.
    """
    _validate_uuid4(correlation_id)
    key = f"{_KEY_PREFIX}{correlation_id}"
    _redis_client.delete(key)