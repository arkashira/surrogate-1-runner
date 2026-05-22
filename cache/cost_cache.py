import time
import threading
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Hashable, Optional, Tuple, TypeVar

# ----------------------------------------------------------------------
# 1️⃣  Typed payload for cost information (from Candidate 2)
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class CostData:
    """Immutable container for a single cost record."""
    service: str          # e.g. "AmazonEC2"
    amount: float         # monetary amount
    start_time: str       # ISO‑8601 timestamp string
    end_time: str         # ISO‑8601 timestamp string


# ----------------------------------------------------------------------
# 2️⃣  Core thread‑safe in‑memory cache with per‑key TTL (from Candidate 1)
# ----------------------------------------------------------------------
T = TypeVar("T")                     # generic payload type

DEFAULT_TTL = 5 * 60                 # 5 minutes, can be overridden per instance


class InMemoryCache(Generic[T]):
    """
    A tiny, thread‑safe cache that stores *any* Python object under a hashable key.
    Each entry lives for ``ttl`` seconds; after that it is considered expired and
    removed on the next access.
    """

    def __init__(self, ttl: int = DEFAULT_TTL):
        self._ttl = ttl
        self._store: Dict[Hashable, Tuple[float, T]] = {}
        self._lock = threading.RLock()

    # ---------- internal helpers ----------
    def _is_expired(self, timestamp: float) -> bool:
        return (time.time() - timestamp) > self._ttl

    # ---------- public API ----------
    def get(self, key: Hashable) -> T:
        """Return the cached value for *key* or raise ``KeyError`` if missing/expired."""
        with self._lock:
            ts, value = self._store[key]          # may raise KeyError
            if self._is_expired(ts):
                del self._store[key]
                raise KeyError(key)
            return value

    def set(self, key: Hashable, value: T) -> None:
        """Store *value* under *key* with the current timestamp."""
        with self._lock:
            self._store[key] = (time.time(), value)

    def clear(self) -> None:
        """Remove **all** entries."""
        with self._lock:
            self._store.clear()

    def __contains__(self, key: Hashable) -> bool:
        """True iff *key* exists **and** is not expired."""
        with self._lock:
            if key not in self._store:
                return False
            ts, _ = self._store[key]
            if self._is_expired(ts):
                del self._store[key]
                return False
            return True