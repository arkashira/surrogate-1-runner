"""
Alert threshold configuration module.

This module provides a simple, extensible way to configure alert thresholds
per notification channel (e.g. email, sms).  Thresholds are expressed as a
percentage increase over the industry benchmark that will trigger an alert.
The configuration can be supplied via an environment variable
`ALERT_THRESHOLDS_JSON` containing a JSON object, or it will fall back to
a sensible default.

The module also exposes a helper to persist historical benchmark data
for the last 90 days.  The data is stored in a lightweight SQLite database
located in the same directory as this module.  The database schema is
created on first use.

Usage
------
>>> from alerts.config import get_threshold, record_benchmark, get_recent_benchmarks
>>> threshold = get_threshold('email')  # returns a float (e.g. 20.0)
>>> record_benchmark('email', 15.3)     # stores a benchmark value
>>> recent_benchmarks = get_recent_benchmarks('email', 7)  # returns a list of benchmark values within the last 7 days
"""

import json
import os
import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration loading
# --------------------------------------------------------------------------- #

_DEFAULT_THRESHOLDS: Dict[str, float] = {
    "email": 20.0,  # percent above benchmark
    "sms": 20.0,
    "slack": 20.0,
}

_ENV_VAR = "ALERT_THRESHOLDS_JSON"

def _load_thresholds() -> Dict[str, float]:
    """
    Load thresholds from the environment variable or fall back to defaults.
    The environment variable should contain a JSON object mapping channel names
    to percentage thresholds.
    """
    raw = os.getenv(_ENV_VAR)
    if not raw:
        return _DEFAULT_THRESHOLDS.copy()

    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("ALERT_THRESHOLDS_JSON must be a JSON object")
        # Validate values
        thresholds = {}
        for channel, value in data.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"Threshold for channel '{channel}' must be numeric")
            thresholds[channel] = float(value)
        return thresholds
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in { _ENV_VAR }: {exc}") from exc

# Load once at import time
_THRESHOLDS: Dict[str, float] = _load_thresholds()

def get_threshold(channel: str) -> float:
    """
    Return the alert threshold for the given channel.
    Raises KeyError if the channel is not configured.
    """
    return _THRESHOLDS[channel]

def set_threshold(channel: str, value: float) -> None:
    """
    Update the threshold for a channel at runtime.
    """
    _THRESHOLDS[channel] = float(value)

# --------------------------------------------------------------------------- #
# Historical benchmark persistence
# --------------------------------------------------------------------------- #

_DB_PATH = Path(__file__).parent / "benchmark_history.db"
_LOCK = threading.Lock()

def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS benchmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL,
            value REAL NOT NULL,
            recorded_at TIMESTAMP NOT NULL
        )
        """
    )
    conn.commit()
    return conn

def record_benchmark(channel: str, value: float) -> None:
    """
    Persist a benchmark value for a channel with the current timestamp.
    """
    with _LOCK:
        conn = _get_connection()
        conn.execute(
            "INSERT INTO benchmarks (channel, value, recorded_at) VALUES (?, ?, ?)",
            (channel, float(value), datetime.utcnow()),
        )
        conn.commit()
        conn.close()

def _purge_old_records() -> None:
    """
    Delete records older than 90 days.
    """
    cutoff = datetime.utcnow() - timedelta(days=90)
    with _LOCK:
        conn = _get_connection()
        conn.execute(
            "DELETE FROM benchmarks WHERE recorded_at < ?",
            (cutoff,),
        )
        conn.commit()
        conn.close()

# Schedule periodic purge (simple approach: purge on each record)
def record_benchmark(channel: str, value: float) -> None:
    """
    Persist a benchmark value for a channel with the current timestamp.
    Also purges any records older than 90 days.
    """
    with _LOCK:
        conn = _get_connection()
        conn.execute(
            "INSERT INTO benchmarks (channel, value, recorded_at) VALUES (?, ?, ?)",
            (channel, float(value), datetime.utcnow()),
        )
        conn.commit()
        conn.close()
    _purge_old_records()

def get_recent_benchmarks(channel: str, days: int = 90) -> list[float]:
    """
    Retrieve benchmark values for the given channel within the last `days`.
    """
    cutoff = datetime.utcnow() - timedelta(days=days)
    with _LOCK:
        conn = _get_connection()
        cur = conn.execute(
            "SELECT value FROM benchmarks WHERE channel = ? AND recorded_at >= ?",
            (channel, cutoff),
        )
        rows = cur.fetchall()
        conn.close()
    return [row[0] for row in rows]