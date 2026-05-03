import sqlite3
from pathlib import Path

_DB_PATH = Path(__file__).parent.parent / "dedup.db"

def _ensure_db() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.execute("CREATE TABLE IF NOT EXISTS seen (md5 TEXT PRIMARY KEY)")
    conn.commit()
    return conn

def is_duplicate(md5: str) -> bool:
    conn = _ensure_db()
    cur = conn.execute("SELECT 1 FROM seen WHERE md5 = ?", (md5,))
    exists = cur.fetchone() is not None
    if not exists:
        conn.execute("INSERT INTO seen (md5) VALUES (?)", (md5,))
        conn.commit()
    conn.close()
    return exists