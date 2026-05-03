import os
import sqlite3
from pathlib import Path
from typing import Optional

def get_db() -> sqlite3.Connection:
    db_path = os.getenv("DEDUP_DB", str(Path(__file__).parent.parent / "dedup.sqlite"))
    conn = sqlite3.connect(db_path, timeout=30)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS seen_hashes ("
        "  md5 TEXT PRIMARY KEY,"
        "  ts DATETIME DEFAULT CURRENT_TIMESTAMP"
        ")"
    )
    conn.commit()
    return conn

def is_duplicate(conn: sqlite3.Connection, md5_hex: str) -> bool:
    cur = conn.execute("SELECT 1 FROM seen_hashes WHERE md5=?", (md5_hex,))
    return cur.fetchone() is not None

def mark_seen(conn: sqlite3.Connection, md5_hex: str) -> None:
    try:
        conn.execute("INSERT INTO seen_hashes (md5) VALUES (?)", (md5_hex,))
    except sqlite3.IntegrityError:
        pass  # race ok