"""
Context Manager for Agent Workflows.

A lightweight, in‑memory, thread‑safe store that keeps a *per‑step*
history of context snapshots.  Each snapshot is immutable and
identified by a monotonically increasing integer.

The module also exposes a small set of convenience functions that
delegate to the singleton instance.  For production you can
subclass :class:`BaseContextStore` and swap the backend.
"""

from __future__ import annotations

import copy
import threading
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class ContextVersion:
    """A single, immutable snapshot of a step’s context."""
    version: int
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StepContext:
    """Keeps all versions for a particular workflow step."""
    step_id: str
    _versions: List[ContextVersion] = field(default_factory=list)

    # --------------------------------------------------------------------- #
    # Mutating helpers – called only by the store
    # --------------------------------------------------------------------- #
    def _add_version(self, data: Dict[str, Any]) -> ContextVersion:
        new_version = len(self._versions) + 1
        snapshot = ContextVersion(new_version, copy.deepcopy(data))
        self._versions.append(snapshot)
        return snapshot

    def _clear(self) -> None:
        self._versions.clear()

    # --------------------------------------------------------------------- #
    # Read helpers – used by the store
    # --------------------------------------------------------------------- #
    def latest(self) -> Optional[ContextVersion]:
        return self._versions[-1] if self._versions else None

    def get(self, version: int) -> Optional[ContextVersion]:
        for v in self._versions:
            if v.version == version:
                return v
        return None

    def list_versions(self) -> List[int]:
        return [v.version for v in self._versions]