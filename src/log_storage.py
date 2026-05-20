"""
Thread‑safe in‑memory log storage for upstream API requests.

The storage holds :class:`LogEntry` records and provides:
* ``add_entry`` – store a new log entry (real‑time update)
* ``query`` – retrieve entries filtered by arbitrary keyword arguments
  (e.g. ``user_id``, ``endpoint``, ``method``).

The implementation is deliberately lightweight to avoid external
dependencies; it can be swapped for a persistent backend later without
changing the public API.
"""

import threading
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class LogEntry:
    """Immutable record of a single upstream API interaction."""
    timestamp: float          # Unix epoch seconds with sub‑second precision
    user_id: str              # Identifier of the user that triggered the request
    method: str               # HTTP method (GET, POST, …)
    endpoint: str             # Full URL of the upstream request
    request_body: Optional[bytes]  # Raw request payload (may be ``None``)
    signature: str           # Cryptographic signature of the request
    response_status: int     # HTTP status code returned by the upstream service
    response_body: Optional[bytes]  # Raw response payload (may be ``None``)


class LogStorage:
    """Singleton‑style thread‑safe container for :class:`LogEntry` objects."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Ensure a single shared instance across the process.
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._entries = []          # type: List[LogEntry]
                    cls._instance._entries_lock = threading.Lock()
        return cls._instance

    def add_entry(self, entry: LogEntry) -> None:
        """Append a new log entry atomically."""
        with self._entries_lock:
            self._entries.append(entry)

    def query(self, **filters: Any) -> List[LogEntry]:
        """
        Retrieve log entries matching all supplied filter criteria.

        Supported filter keys correspond to ``LogEntry`` fields.
        Example::
            storage.query(user_id="alice", method="POST")
        """
        with self._entries_lock:
            results = self._entries
            for key, value in filters.items():
                if not hasattr(LogEntry, key):
                    raise ValueError(f"Invalid filter field: {key}")
                results = [e for e in results if getattr(e, key) == value]
            # Return a shallow copy to prevent external mutation.
            return list(results)

    def clear(self) -> None:
        """Remove all stored entries – useful for testing."""
        with self._entries_lock:
            self._entries.clear()

    def dump(self) -> List[Dict[str, Any]]:
        """Return a serialisable representation of the log (e.g. for UI)."""
        with self._entries_lock:
            return [asdict(entry) for entry in self._entries]


# Export a module‑level singleton for convenient import.
log_storage = LogStorage()