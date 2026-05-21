import json
import os
import threading
from datetime import datetime
from typing import List, Optional, Dict

# Default location for the audit log.  In production this should be a
# secure, append‑only location with appropriate OS permissions.
DEFAULT_AUDIT_LOG_PATH = "/var/log/axentx/audit.log"

# Allow the path to be overridden (useful for tests).
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", DEFAULT_AUDIT_LOG_PATH)

# Ensure the directory exists.
os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)

# A simple file‑level lock to make appends thread‑safe.
_lock = threading.Lock()


def _write_entry(entry: Dict) -> None:
    """Append a single JSON‑encoded audit entry to the log file."""
    line = json.dumps(entry, separators=(",", ":")) + "\n"
    with _lock, open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)


def log_ai_request(user_id: str, ai_tool: str, request_payload: Dict) -> None:
    """
    Record an AI request for audit purposes.

    Parameters
    ----------
    user_id: str
        Identifier of the user making the request.
    ai_tool: str
        Name or identifier of the AI tool that was invoked.
    request_payload: dict
        The request data (will be stored as‑is; sensitive fields should be
        stripped by the caller before logging).
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "ai_tool": ai_tool,
        "request": request_payload,
    }
    _write_entry(entry)


def get_audit_trail(limit: Optional[int] = None) -> List[Dict]:
    """
    Retrieve audit entries.

    Parameters
    ----------
    limit: int | None
        Maximum number of most‑recent entries to return.  If ``None`` all
        entries are returned.

    Returns
    -------
    List[dict]
        Audit entries ordered from newest to oldest.
    """
    if not os.path.exists(AUDIT_LOG_PATH):
        return []

    with _lock, open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Parse JSON lines; ignore malformed lines to keep the service robust.
    entries = []
    for line in reversed(lines):
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
        if limit is not None and len(entries) >= limit:
            break
    return entries