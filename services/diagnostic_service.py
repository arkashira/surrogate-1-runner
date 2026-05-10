"""
Diagnostic Service
==================

A lightweight, in‑memory diagnostic session store with a 30‑day
expiration policy.

Public API
----------
* DiagnosticService(session_storage)
    * get_diagnostic_result(session_id: str) -> dict
    * add_diagnostic(session_id: str, matched_patterns: list[str], resolution_steps: str) -> None
    * cleanup_expired_sessions() -> None

* InMemorySessionStorage()
    * add(session_id, session_data)
    * get(session_id) -> dict | None

* DiagnosticSessionNotFoundError
    * Raised when a session is missing or expired.

The service is intentionally simple so it can be dropped into a FastAPI
endpoint or any other framework without modification.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #
class DiagnosticSessionNotFoundError(Exception):
    """Raised when a diagnostic session cannot be found or has expired."""


# --------------------------------------------------------------------------- #
# Storage abstraction
# --------------------------------------------------------------------------- #
class InMemorySessionStorage:
    """A minimal in‑memory key/value store for diagnostic sessions."""

    def __init__(self) -> None:
        self._sessions: Dict[str, dict] = {}

    def add(self, session_id: str, session_data: dict) -> None:
        """Store a session. Overwrites if the key already exists."""
        self._sessions[session_id] = session_data

    def get(self, session_id: str) -> Optional[dict]:
        """Return the session data or None if missing."""
        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> None:
        """Remove a session if it exists."""
        self._sessions.pop(session_id, None)

    def all_sessions(self) -> Dict[str, dict]:
        """Return a shallow copy of all sessions (used by cleanup)."""
        return dict(self._sessions)


# --------------------------------------------------------------------------- #
# Service
# --------------------------------------------------------------------------- #
class DiagnosticService:
    """Core diagnostic session logic."""

    EXPIRATION_DAYS = 30
    EXPIRATION_DELTA = timedelta(days=EXPIRATION_DAYS)

    def __init__(self, storage: InMemorySessionStorage) -> None:
        self._storage = storage

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def add_diagnostic(
        self,
        session_id: str,
        matched_patterns: List[str],
        resolution_steps: str,
    ) -> None:
        """Persist a new diagnostic session."""
        session_data = {
            "created_at": datetime.utcnow().isoformat(),
            "matched_patterns": matched_patterns,
            "resolution_steps": resolution_steps,
        }
        self._storage.add(session_id, session_data)

    def get_diagnostic_result(self, session_id: str) -> dict:
        """Return the diagnostic result for *session_id* or raise."""
        session_data = self._storage.get(session_id)
        if session_data is None or self._is_session_expired(session_data):
            raise DiagnosticSessionNotFoundError(
                f"Session {session_id} not found or expired"
            )

        # Return a copy so callers cannot mutate internal state
        return {
            "session_id": session_id,
            "matched_patterns": list(session_data["matched_patterns"]),
            "resolution_steps": session_data["resolution_steps"],
        }

    def cleanup_expired_sessions(self) -> None:
        """Remove all sessions that have outlived the expiration window."""
        now = datetime.utcnow()
        for sid, data in list(self._storage.all_sessions().items()):
            created_at = datetime.fromisoformat(data["created_at"])
            if now > created_at + self.EXPIRATION_DELTA:
                self._storage.delete(sid)

    # --------------------------------------------------------------------- #
    # Internals
    # --------------------------------------------------------------------- #
    def _is_session_expired(self, session_data: dict) -> bool:
        created_at = datetime.fromisoformat(session_data["created_at"])
        return datetime.utcnow() > created_at + self.EXPIRATION_DELTA


# --------------------------------------------------------------------------- #
# Example usage (would normally live in an API layer)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    storage = InMemorySessionStorage()
    service = DiagnosticService(storage)

    # Add a session
    service.add_diagnostic(
        "sess-001",
        ["patternA", "patternB"],
        "## Step 1\nDo something\n\n## Step 2\nDo something else",
    )

    # Retrieve it
    try:
        result = service.get_diagnostic_result("sess-001")
        print("Diagnostic result:", result)
    except DiagnosticSessionNotFoundError as exc:
        print(exc)

    # Cleanup (would normally run in a background task)
    service.cleanup_expired_sessions()