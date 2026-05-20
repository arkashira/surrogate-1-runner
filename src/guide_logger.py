"""
Utility module for logging guide usage and resolution outcomes.

All logs are written as JSON Lines to
/opt/axentx/surrogate-1/logs/guide_usage.log.  Each log entry contains:

- timestamp: ISO 8601 UTC timestamp
- guide_id: Identifier of the guide being used
- user_id: Identifier of the user (or system component) invoking the guide
- outcome: Success or failure string
- details: Optional dictionary with additional context

The module exposes a single function `log_guide_usage` that can be called
from any part of the application.  It is intentionally lightweight and
does not depend on external services, making it safe to use in
resource-constrained workers.
"""

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

# Directory where logs are stored.  It is created on first use.
LOG_DIR = Path("/opt/axentx/surrogate-1/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Path to the log file
LOG_FILE = LOG_DIR / "guide_usage.log"

# A simple thread‑safe file writer
_lock = threading.Lock()


def _write_log_entry(entry: Dict[str, Any]) -> None:
    """
    Append a JSON line to the log file in a thread‑safe manner.
    """
    with _lock:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")


def log_guide_usage(
    guide_id: str,
    user_id: str,
    outcome: str,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log a single guide usage event.

    Parameters
    ----------
    guide_id : str
        Identifier of the guide that was invoked.
    user_id : str
        Identifier of the user or system component that invoked the guide.
    outcome : str
        Outcome of the guide resolution, e.g. "success" or "failure".
    details : dict, optional
        Additional context to include in the log entry.
    """
    entry: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "guide_id": guide_id,
        "user_id": user_id,
        "outcome": outcome,
        "details": details or {},
    }
    _write_log_entry(entry)