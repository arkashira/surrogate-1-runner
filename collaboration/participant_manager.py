import threading
from pathlib import Path
from typing import Set, List

import yaml


class ParticipantManagerError(Exception):
    """Base exception for participant manager errors."""


class ParticipantAlreadyExistsError(ParticipantManagerError):
    """Raised when trying to add a participant that already exists."""


class ParticipantNotFoundError(ParticipantManagerError):
    """Raised when trying to remove a participant that does not exist."""


class ParticipantManager:
    """
    Thread‑safe manager for real‑time terminal collaboration participants.

    The manager reads optional configuration from ``config.yaml`` which can
    define limits such as ``max_participants``.  All operations are protected
    by an internal lock to guarantee consistency across threads.
    """

    def __init__(self, config_path: str | Path = "/opt/axentx/surrogate-1/collaboration/config.yaml"):
        self._lock = threading.RLock()
        self._participants: Set[str] = set()
        self._config_path = Path(config_path)
        self._max_participants: int | None = None
        self._load_config()

    # --------------------------------------------------------------------- #
    # Configuration handling
    # --------------------------------------------------------------------- #
    def _load_config(self) -> None:
        """Load configuration from YAML file if it exists."""
        if not self._config_path.is_file():
            # No config – use defaults
            self._max_participants = None
            return

        with self._config_path.open("r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        self._max_participants = cfg.get("max_participants")

    # --------------------------------------------------------------------- #
    # Participant operations
    # --------------------------------------------------------------------- #
    def add_participant(self, user_id: str) -> None:
        """
        Add a participant to the session.

        Raises:
            ParticipantAlreadyExistsError: if ``user_id`` is already present.
            ParticipantManagerError: if the max participants limit is reached.
        """
        with self._lock:
            if user_id in self._participants:
                raise ParticipantAlreadyExistsError(f"Participant '{user_id}' already added.")
            if self._max_participants is not None and len(self._participants) >= self._max_participants:
                raise ParticipantManagerError(
                    f"Cannot add participant '{user_id}': max participants ({self._max_participants}) reached."
                )
            self._participants.add(user_id)

    def remove_participant(self, user_id: str) -> None:
        """
        Remove a participant from the session.

        Raises:
            ParticipantNotFoundError: if ``user_id`` is not present.
        """
        with self._lock:
            if user_id not in self._participants:
                raise ParticipantNotFoundError(f"Participant '{user_id}' not found.")
            self._participants.remove(user_id)

    def list_participants(self) -> List[str]:
        """
        Return a snapshot list of current participants, sorted for deterministic output.
        """
        with self._lock:
            return sorted(self._participants)

    # --------------------------------------------------------------------- #
    # Utility helpers (optional for external callers)
    # --------------------------------------------------------------------- #
    def is_participant(self, user_id: str) -> bool:
        """Check if a user is currently a participant."""
        with self._lock:
            return user_id in self._participants

    def clear(self) -> None:
        """Remove all participants – primarily for testing or session reset."""
        with self._lock:
            self._participants.clear()