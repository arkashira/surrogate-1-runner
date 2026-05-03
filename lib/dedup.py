import sqlite3
import os
import threading

class DedupStore:
    def __init__(self, db_path=None):
        # Use central store path if provided by env; otherwise local temp.
        self.db_path = db_path or os.getenv("DEDUP_DB", ":memory:")
        self._lock = threading.Lock()
        self._init()

    def _init(self):
        with self._lock, sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS seen (md5 TEXT PRIMARY KEY)")

    def seen(self, md5):
        with self._lock, sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT 1 FROM seen WHERE md5=?", (md5,))
            return cur.fetchone() is not None

    def add(self, md5):
        with self._lock, sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR IGNORE INTO seen (md5) VALUES (?)", (md5,))