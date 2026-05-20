"""Migration to add baseline_response field to model_runs table."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "models.db"

def migrate():
    """Add baseline_response column to model_runs if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if column exists
    cursor.execute("PRAGMA table_info(model_runs)")
    columns = [column[1] for column in cursor.fetchall()]

    if "baseline_response" not in columns:
        cursor.execute("ALTER TABLE model_runs ADD COLUMN baseline_response TEXT")
        print("Added baseline_response column to model_runs")
    else:
        print("baseline_response column already exists")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()