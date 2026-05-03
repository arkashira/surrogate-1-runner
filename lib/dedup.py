import sqlite3
from pathlib import Path
from contextlib import contextmanager

class DedupStore:
    def __init__(self, db_path: str = ".dedup.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS seen_pair (hash TEXT PRIMARY KEY)")

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        try:
            yield conn
        finally:
            conn.close()

    def add(self, pair_hash: str) -> bool:
        """Return True if newly inserted, False if duplicate."""
        cur = self._conn().__enter__().cursor()
        try:
            cur.execute("INSERT INTO seen_pair (hash) VALUES (?)", (pair_hash,))
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            cur.close()

    def bulk_contains(self, hashes):
        if not hashes:
            return set()
        cur = self._conn().__enter__().cursor()
        cur.execute(f"SELECT hash FROM seen_pair WHERE hash IN ({','.join('?'*len(hashes))})", hashes)
        return {row[0] for row in cur.fetchall()}