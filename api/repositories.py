import asyncio
from dataclasses import field, dataclass
from datetime import datetime
from typing import Dict, List
import uuid


@dataclass
class InMemoryViolationRepository:
    """Simple in‑memory store – replace with a real DB in production."""
    _store: Dict[str, List[Violation]] = field(default_factory=dict)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def get_by_account(
        self,
        account_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Violation]:
        async with self._lock:
            violations = self._store.get(account_id, [])
        # Sort newest first
        sorted_violations = sorted(violations, key=lambda v: v.timestamp, reverse=True)
        return sorted_violations[offset : offset + limit]

    async def add(self, violation: Violation) -> None:
        async with self._lock:
            self._store.setdefault(violation.account_id, []).append(violation)