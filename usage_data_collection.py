import os
import json
import sqlite3
import random
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
# Directory to store the SQLite DB.  Created if missing.
DATA_DIR = os.getenv("USAGE_DATA_DIR", "/opt/axentx/surrogate-1/data")
DB_PATH = os.path.join(DATA_DIR, "usage.db")

# Optional path to a JSON file that contains mock historical usage.
# If the file exists, its contents are used instead of random generation.
MOCK_USAGE_JSON = os.getenv("MOCK_USAGE_JSON", "")

# ----------------------------------------------------------------------
# SQLite schema
# ----------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS usage_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    service TEXT NOT NULL,
    usage_amount REAL NOT NULL,
    cost REAL NOT NULL
);
"""

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _ensure_db() -> sqlite3.Connection:
    """Create the data directory and initialise the DB if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def _load_mock_usage() -> List[Dict[str, Any]]:
    """Load mock usage records from a JSON file if configured."""
    if MOCK_USAGE_JSON and os.path.isfile(MOCK_USAGE_JSON):
        with open(MOCK_USAGE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    return []


def _generate_random_usage(num_records: int = 10) -> List[Dict[str, Any]]:
    """Generate a list of synthetic usage records."""
    services = ["compute", "storage", "network", "database"]
    now = datetime.now(timezone.utc)
    records = []
    for _ in range(num_records):
        ts = now - timedelta(minutes=random.randint(0, 1440))
        service = random.choice(services)
        usage_amount = round(random.uniform(0.1, 100.0), 2)
        # Simple cost model: $0.02 per unit of usage
        cost = round(usage_amount * 0.02, 2)
        records.append(
            {
                "ts": ts.isoformat(),
                "service": service,
                "usage_amount": usage_amount,
                "cost": cost,
            }
        )
    return records


def collect_usage() -> List[Dict[str, Any]]:
    """
    Collect historical usage data.

    The function first attempts to load mock data from ``MOCK_USAGE_JSON``.
    If the file is absent or empty, it falls back to generating a small
    random sample.  In a production environment this function would be
    replaced with real cloud‑provider API calls.
    """
    mock = _load_mock_usage()
    if mock:
        return mock
    return _generate_random_usage()


def store_usage(records: List[Dict[str, Any]]) -> None:
    """
    Persist a list of usage records into the SQLite database.

    Args:
        records: List of dictionaries with keys ``ts``, ``service``,
                 ``usage_amount`` and ``cost``.
    """
    if not records:
        return

    conn = _ensure_db()
    cur = conn.cursor()
    insert_sql = """
        INSERT INTO usage_records (ts, service, usage_amount, cost)
        VALUES (:ts, :service, :usage_amount, :cost);
    """
    cur.executemany(insert_sql, records)
    conn.commit()
    conn.close()


def daily_update() -> None:
    """
    Entry point for the daily job.

    Collects usage data and stores it.  Designed to be invoked by a
    scheduler (e.g., cron, GitHub Actions, Airflow) once per day.
    """
    records = collect_usage()
    store_usage(records)


if __name__ == "__main__":
    daily_update()