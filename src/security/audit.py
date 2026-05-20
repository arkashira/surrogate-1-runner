"""
Audit logger for Surrogate.

* One‑line JSON records written to a file that is rotated daily and kept
  for 30 days.
* Each record contains:
    - timestamp (ISO‑8601 UTC)
    - user_id
    - correlation_id
    - workflow_name
    - request_hash (SHA‑256 of the *exact* request payload)
    - checksum (SHA‑256 of the JSON line **without** the checksum field,
      giving tamper‑evidence)
* The log file location can be overridden with the ``AUDIT_LOG_PATH``
  environment variable – useful for CI, tests or custom deployments.
* The public API is a single function ``log_submission`` that can be called
  from anywhere in the code‑base.
"""

import json
import hashlib
import os
from datetime import datetime, timezone
from typing import Any, Dict

from loguru import logger

# ----------------------------------------------------------------------
# 1️⃣  Configuration
# ----------------------------------------------------------------------
DEFAULT_LOG_PATH = "/var/log/surrogate/audit.log"
LOG_PATH = os.getenv("AUDIT_LOG_PATH", DEFAULT_LOG_PATH)

# Loguru adds a handler only once – guard against double‑initialisation
if not any(getattr(h, "path", None) == LOG_PATH for h in logger.handlers):
    # Remove the default stderr handler that Loguru creates automatically
    logger.remove()
    logger.add(
        LOG_PATH,
        level="INFO",
        format="{message}",          # we write a complete JSON line ourselves
        rotation="00:00",            # rotate at midnight (daily)
        retention="30 days",         # keep 30 days of history
        compression="gz",            # compress old files to save space
        enqueue=True,                # thread‑safe, non‑blocking
        backtrace=False,
        diagnose=False,
    )

# ----------------------------------------------------------------------
# 2️⃣  Helper utilities
# ----------------------------------------------------------------------
def _hash_request(request_body: Any) -> str:
    """
    Return a deterministic SHA‑256 hash of the request payload.

    * If the payload is JSON‑serialisable we dump it with ``sort_keys=True``
      and the most compact separators – this guarantees that two equal
      Python objects produce the same hash even if their original string
      representation differed.
    * For non‑JSON payloads we fall back to ``str(payload)``.
    """
    if isinstance(request_body, (dict, list)):
        serialized = json.dumps(request_body, sort_keys=True, separators=(",", ":"))
    else:
        serialized = str(request_body)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _checksum_of_line(json_line_without_checksum: str) -> str:
    """
    Compute the SHA‑256 checksum of a *complete* JSON line **excluding**
    the ``checksum`` field.  The caller must have already serialised the
    record without the checksum key.
    """
    return hashlib.sha256(json_line_without_checksum.encode("utf-8")).hexdigest()


def _build_log_record(
    user_id: str,
    correlation_id: str,
    workflow_name: str,
    request_body: Any,
) -> Dict[str, Any]:
    """
    Assemble the dictionary that will become the audit line.
    The checksum is calculated after the rest of the fields have been
    serialised, then injected back into the dict.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    request_hash = _hash_request(request_body)

    # Base record – *without* checksum
    record = {
        "timestamp": timestamp,
        "user_id": user_id,
        "correlation_id": correlation_id,
        "workflow_name": workflow_name,
        "request_hash": request_hash,
    }

    # Serialize the record (compact, deterministic) to compute checksum
    partial_line = json.dumps(record, separators=(",", ":"), sort_keys=True)
    record["checksum"] = _checksum_of_line(partial_line)

    return record


# ----------------------------------------------------------------------
# 3️⃣  Public API
# ----------------------------------------------------------------------
def log_submission(
    user_id: str,
    correlation_id: str,
    workflow_name: str,
    request_body: Any,
) -> None:
    """
    Write a single immutable audit line.

    Example usage::

        from src.security.audit import log_submission

        log_submission(
            user_id="alice",
            correlation_id="123e4567-e89b-12d3-a456-426614174000",
            workflow_name="create_invoice",
            request_body={"amount": 100, "currency": "USD"},
        )
    """
    record = _build_log_record(
        user_id=user_id,
        correlation_id=correlation_id,
        workflow_name=workflow_name,
        request_body=request_body,
    )
    # ``logger.info`` writes the *exact* string we give it – no extra
    # formatting, no newline handling needed.
    logger.info(json.dumps(record, separators=(",", ":"), sort_keys=True))


# Export only the public function – helpers stay private.
__all__ = ["log_submission"]