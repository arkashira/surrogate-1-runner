"""
Immutable audit logger for Surrogate.

Each log line is a single JSON object that contains:

    * timestamp (ISO‑8601 UTC)
    * user_id
    * correlation_id
    * workflow_name
    * request_hash (SHA‑256 of the raw HTTP body)
    * checksum (SHA‑256 of the JSON *without* this field)

The file is rotated automatically at midnight (UTC) and kept for 30 days.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Configuration – change only if you have a different log location or policy #
# --------------------------------------------------------------------------- #
LOG_DIR = Path("/var/log/surrogate")
LOG_FILE = LOG_DIR / "audit.log"
RETENTION_DAYS = 30          # how many rotated files to keep
UTC = timezone.utc

# Ensure the directory exists before the logger is created.
LOG_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
# Helper: compute a SHA‑256 checksum of a string (used for the immutable line) #
# --------------------------------------------------------------------------- #
def _checksum(text: str) -> str:
    """Return a hex SHA‑256 checksum of *text*."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Logger setup – a TimedRotatingFileHandler that rotates at midnight UTC      #
# --------------------------------------------------------------------------- #
_logger = logging.getLogger("surrogate.audit")
_logger.setLevel(logging.INFO)

# The handler writes **only** the message (no extra metadata) – we already
# embed everything we need in the JSON payload.
_handler = logging.handlers.TimedRotatingFileHandler(
    filename=str(LOG_FILE),
    when="midnight",
    utc=True,
    backupCount=RETENTION_DAYS,
)
_handler.suffix = "%Y-%m-%d"          # e.g. audit.log.2024-09-01
_handler.extMatch = logging.handlers._TimedRotatingFileHandler.extMatch  # type: ignore
_handler.setFormatter(logging.Formatter("%(message)s"))  # raw line
_logger.addHandler(_handler)


# --------------------------------------------------------------------------- #
# Public API – call this from anywhere in the code base                         #
# --------------------------------------------------------------------------- #
def write_audit_record(
    *,
    user_id: str,
    correlation_id: str,
    workflow_name: str,
    request_hash: str,
) -> None:
    """
    Append a single immutable audit record.

    The function is deliberately tiny and synchronous – the surrounding
    FastAPI endpoint is already async, but the I/O cost of a single line
    append is negligible (< 1 ms) and does not block the event loop
    appreciably.  If you ever need true async I/O, replace the ``_logger.info``
    call with an ``await loop.run_in_executor`` wrapper.

    Parameters
    ----------
    user_id:
        Identifier of the authenticated user that triggered the request.
    correlation_id:
        Business‑level correlation identifier supplied by the client.
    workflow_name:
        Name of the workflow being submitted.
    request_hash:
        SHA‑256 of the raw request body – useful for later replay or
        forensic checks.
    """
    # Build the payload *without* the checksum first.
    payload: Dict[str, Any] = {
        "timestamp": datetime.now(UTC).isoformat(),
        "user_id": user_id,
        "correlation_id": correlation_id,
        "workflow_name": workflow_name,
        "request_hash": request_hash,
    }

    # Serialize compactly (no spaces) so the checksum is deterministic.
    line_without_checksum = json.dumps(payload, separators=(",", ":"))
    payload["checksum"] = _checksum(line_without_checksum)

    # Final line – again compact, then a newline is added by the logger.
    final_line = json.dumps(payload, separators=(",", ":"))
    _logger.info(final_line)          # type: ignore[arg-type]