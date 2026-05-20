"""
Monitoring component that simulates fetching firewall validation
statuses.  In a real deployment this would interface with the
firewall APIs and validation logic.

The module exposes a single coroutine `get_latest_status()` that
returns a dictionary.  The implementation below is intentionally
deterministic enough for unit tests but still shows how you could
swap it out for a real API call.

Design notes
------------
* The status is cached for 30 s to avoid hammering the real API.
* The mock rotates severity every 5 updates to demonstrate change.
"""

from __future__ import annotations

import random
import time
from typing import Dict, Any

# In‑memory cache
_last_status: Dict[str, Any] | None = None
_last_update: float = 0.0
_CACHE_TTL: float = 30.0  # seconds


def _generate_mock_status() -> Dict[str, Any]:
    """Return a deterministic‑looking mock status."""
    now = time.time()
    severity = random.choice(["info", "warning", "critical"])
    rule_id = f"RULE-{random.randint(1000, 9999)}"
    status = {
        "firewall": f"FW-{random.randint(1, 5)}",
        "rule": rule_id,
        "severity": severity,
        "message": f"Mock validation result for {rule_id}",
        "timestamp": now,
    }
    return status


async def get_latest_status() -> Dict[str, Any]:
    """
    Return the latest validation status.

    If more than `_CACHE_TTL` seconds have elapsed since the last
    update, a new status is generated.  In production this function
    would call the real firewall API instead of generating a mock.
    """
    global _last_status, _last_update
    if _last_status is None or time.time() - _last_update > _CACHE_TTL:
        _last_status = _generate_mock_status()
        _last_update = time.time()
    return _last_status