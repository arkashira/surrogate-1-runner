from __future__ import annotations
import time
import threading
import heapq
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Tuple, List, Callable

# ----------------------------------------------------------------------
# 1.1  TTL Policy
# ----------------------------------------------------------------------
class TTLPolicy(Enum):
    NEVER = "never"          # never expires
    FIXED = "fixed"          # expires after a fixed duration
    SLIDING = "sliding"      # expires after duration of inactivity
    WORKFLOW = "workflow"    # expires when workflow ends
    INHERIT = "inherit"      # inherits policy/value from parent

# ----------------------------------------------------------------------
# 1.2  TTL Configuration
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TTLConfig:
    policy: TTLPolicy = TTLPolicy.INHERIT
    duration_seconds: Optional[int] = None   # required for FIXED/SLIDING
    inherit_from_parent: bool = True

    def __post_init__(self):
        if self.policy in {TTLPolicy.FIXED, TTLPolicy.SLIDING}:
            if not self.duration_seconds or self.duration_seconds <= 0:
                raise ValueError(f"duration_seconds must be >0 for {self.policy}")

# ----------------------------------------------------------------------
# 1.3  Context Variable Entry
# ----------------------------------------------------------------------
@dataclass
class ContextEntry:
    key: str
    value: Any
    ttl_config: TTLConfig
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    parent_context_id: Optional[str] = None
    # For heap ordering
    _expiry_ts: float = field(init=False, compare=True)

    def __post_init__(self):
        self._expiry_ts = self._compute_expiry()

    # ------------------------------------------------------------------
    # 1.3.1  Expiry calculation
    # ------------------------------------------------------------------
    def _compute_expiry(self) -> float:
        if self.ttl_config.policy == TTLPolicy.NEVER:
            return float("inf")
        if self.ttl_config.policy == TTLPolicy.WORKFLOW:
            return float("inf")   # handled by workflow manager
        if self.ttl_config.policy == TTLPolicy.INHERIT:
            return float("inf")   # resolved during lookup
        now = time.time()
        if self.ttl_config.policy == TTLPolicy.FIXED:
            return self.created_at + self.ttl_config.duration_seconds
        if self.ttl_config.policy == TTLPolicy.SLIDING:
            return self.last_accessed + self.ttl_config.duration_seconds
        return float("inf")

    # ------------------------------------------------------------------
    # 1.3.2  Refresh for sliding TTL
    # ------------------------------------------------------------------
    def touch(self) -> None:
        if self.ttl_config.policy == TTLPolicy.SLIDING:
            self.last_accessed = time.time()
            self._expiry_ts = self._compute_expiry()

    # ------------------------------------------------------------------
    # 1.3.3  Expiry check
    # ------------------------------------------------------------------
    def is_expired(self) -> bool:
        return time.time() >= self._expiry_ts