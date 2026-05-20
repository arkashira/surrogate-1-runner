import sqlite3
from pathlib import Path
from typing import Iterable, Tuple, Any

DB_PATH = Path("/opt/axentx/surrogate-1/data/cost.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS cost_records (
    provider   TEXT NOT NULL,
    timestamp  TEXT NOT NULL,          -- ISO‑8601 UTC, start of aggregation window
    amount_usd REAL NOT NULL,
    metadata   TEXT,                   -- JSON string, optional
    PRIMARY KEY (provider, timestamp)
);
"""

def init_db() -> None:
    """Create the table if it does not exist.  Safe to call repeatedly."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(_SCHEMA)

def bulk_upsert(records: Iterable[Tuple[str, str, float, str]]) -> None:
    """
    Insert many rows, ignoring duplicates (PK violation).
    ``records`` is an iterable of (provider, timestamp, amount_usd, metadata_json).
    """
    if not records:
        return
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.executemany(
            """
            INSERT INTO cost_records (provider, timestamp, amount_usd, metadata)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(provider, timestamp) DO NOTHING;
            """,
            records,
        )
        conn.commit()