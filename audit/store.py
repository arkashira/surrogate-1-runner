"""
Simple audit‑log storage backed by a JSON‑lines file.

The file is appended to for every new entry.  Querying is performed by
reading the file and filtering in memory.  For production workloads a
dedicated database or log aggregation system would be preferable.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Iterable, List, Optional

from .schema import AuditEntry

# ----------------------------------------------------------------------
# Configuration – can be overridden by the environment
# ----------------------------------------------------------------------
DEFAULT_LOG_DIR = Path("/opt/axentx/surrogate-1/logs")
LOG_DIR = Path(os.getenv("AUDIT_LOG_DIR", DEFAULT_LOG_DIR))
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "audit.log"

# ----------------------------------------------------------------------
# Core helpers
# ----------------------------------------------------------------------
def append(entry: AuditEntry) -> None:
    """Append a single audit entry to the log file."""
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(entry.to_json() + "\n")

def _iter_entries() -> Iterable[AuditEntry]:
    """Yield all entries from the log file."""
    if not LOG_FILE.exists():
        return
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield AuditEntry.from_json(line)

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def query(
    service: Optional[str] = None,
    cluster: Optional[str] = None,
) -> List[AuditEntry]:
    """
    Return all entries matching the optional service and/or cluster filters.
    """
    results: List[AuditEntry] = []
    for entry in _iter_entries():
        if service and entry.service != service:
            continue
        if cluster and entry.cluster != cluster:
            continue
        results.append(entry)
    return results

def export_csv(
    filepath: str | Path,
    service: Optional[str] = None,
    cluster: Optional[str] = None,
) -> None:
    """
    Export filtered audit entries to a CSV file.

    The CSV columns are: timestamp,service,cluster,action,details (JSON string).
    """
    entries = query(service, cluster)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "service", "cluster", "action", "details"])
        for e in entries:
            writer.writerow(
                [e.timestamp, e.service, e.cluster, e.action, json.dumps(e.details, ensure_ascii=False)]
            )