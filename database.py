import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

# Path to the SQLite database file (placed alongside this module)
DB_PATH = Path(__file__).with_name("templates.db")

def _get_connection() -> sqlite3.Connection:
    """Create a new SQLite connection with row factory for dict‑like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize the templates table if it does not already exist."""
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS templates (
                name TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                steps TEXT NOT NULL
            )
            """
        )
        conn.commit()

# Ensure the DB is ready on import
init_db()

def _serialize_steps(steps: List[Any]) -> str:
    return json.dumps(steps)

def _deserialize_steps(steps_json: str) -> List[Any]:
    return json.loads(steps_json)

def save_template(name: str, description: str, steps: List[Any]) -> None:
    """Insert a new template or replace an existing one (upsert)."""
    steps_json = _serialize_steps(steps)
    with _get_connection() as conn:
        conn.execute(
            """
            INSERT INTO templates (name, description, steps)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                description=excluded.description,
                steps=excluded.steps
            """,
            (name, description, steps_json),
        )
        conn.commit()

def get_template(name: str) -> Optional[Dict[str, Any]]:
    """Retrieve a template record by name. Returns None if not found."""
    with _get_connection() as conn:
        cur = conn.execute(
            "SELECT name, description, steps FROM templates WHERE name = ?", (name,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {
            "name": row["name"],
            "description": row["description"],
            "steps": _deserialize_steps(row["steps"]),
        }

def add_step(name: str, step: Any) -> None:
    """Append a step to the stored template."""
    tmpl = get_template(name)
    if tmpl is None:
        raise ValueError(f"Template '{name}' does not exist.")
    steps = tmpl["steps"]
    steps.append(step)
    save_template(name, tmpl["description"], steps)

def remove_step(name: str, index: int) -> None:
    """Remove a step at *index* from the stored template."""
    tmpl = get_template(name)
    if tmpl is None:
        raise ValueError(f"Template '{name}' does not exist.")
    steps = tmpl["steps"]
    if not (0 <= index < len(steps)):
        raise IndexError("Step index out of range.")
    del steps[index]
    save_template(name, tmpl["description"], steps)