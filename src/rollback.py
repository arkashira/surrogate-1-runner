"""
Rollback functionality for surrogate-1.

This module provides a simple one‑click rollback for the current model
version and prompt state.  The current state is stored in the
`current_state` table, and all rollbacks are recorded in
`rollback_history`.  The CLI exposes two sub‑commands:

* `rollback-model` – Reverts the current model to the previous version.
* `rollback-prompt` – Reverts the current prompt to the previous state.

The module is intentionally lightweight and uses SQLite directly.
"""

import argparse
import datetime
import os
import sqlite3
import sys
from contextlib import contextmanager
from typing import Optional, Tuple

DB_PATH = os.getenv("SURROGATE_DB", "/opt/axentx/surrogate-1/db/surrogate.db")


@contextmanager
def get_connection(db_path: str = DB_PATH):
    """Yield a SQLite connection, ensuring commit/rollback."""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _fetch_current(conn: sqlite3.Connection, state_type: str) -> Optional[int]:
    """Return the current id for the given state_type (`model` or `prompt`)."""
    cur = conn.execute(
        "SELECT current_id FROM current_state WHERE state_type = ?", (state_type,)
    )
    row = cur.fetchone()
    return row[0] if row else None


def _update_current(conn: sqlite3.Connection, state_type: str, new_id: int):
    """Update the current id for the given state_type."""
    conn.execute(
        """
        INSERT INTO current_state (state_type, current_id)
        VALUES (?, ?)
        ON CONFLICT(state_type) DO UPDATE SET current_id = excluded.current_id
        """,
        (state_type, new_id),
    )


def _record_rollback(
    conn: sqlite3.Connection, state_type: str, from_id: int, to_id: int
):
    """Insert a rollback record."""
    conn.execute(
        """
        INSERT INTO rollback_history
        (state_type, from_id, to_id, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (state_type, from_id, to_id, datetime.datetime.utcnow().isoformat()),
    )


def _get_latest_rollback(conn: sqlite3.Connection, state_type: str) -> Optional[Tuple[int, int]]:
    """
    Return the most recent rollback (from_id, to_id) for the given state_type.
    """
    cur = conn.execute(
        """
        SELECT from_id, to_id
        FROM rollback_history
        WHERE state_type = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (state_type,),
    )
    row = cur.fetchone()
    return (row[0], row[1]) if row else None


def rollback_model(conn: sqlite3.Connection):
    """Rollback the current model to the previous version."""
    current_id = _fetch_current(conn, "model")
    if current_id is None:
        raise RuntimeError("No current model set.")
    latest = _get_latest_rollback(conn, "model")
    if latest is None:
        raise RuntimeError("No rollback history for model.")
    from_id, to_id = latest
    if to_id != current_id:
        raise RuntimeError(
            f"Rollback history mismatch: current model id {current_id} "
            f"does not match expected {to_id}."
        )
    # Find the previous version before the current one
    cur = conn.execute(
        """
        SELECT id FROM model_versions
        WHERE id < ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (current_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("No earlier model version to rollback to.")
    new_id = row[0]
    _update_current(conn, "model", new_id)
    _record_rollback(conn, "model", current_id, new_id)
    print(f"Rolled back model from {current_id} to {new_id}.")


def rollback_prompt(conn: sqlite3.Connection):
    """Rollback the current prompt to the previous state."""
    current_id = _fetch_current(conn, "prompt")
    if current_id is None:
        raise RuntimeError("No current prompt set.")
    latest = _get_latest_rollback(conn, "prompt")
    if latest is None:
        raise RuntimeError("No rollback history for prompt.")
    from_id, to_id = latest
    if to_id != current_id:
        raise RuntimeError(
            f"Rollback history mismatch: current prompt id {current_id} "
            f"does not match expected {to_id}."
        )
    # Find the previous prompt before the current one
    cur = conn.execute(
        """
        SELECT id FROM prompts
        WHERE id < ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (current_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("No earlier prompt to rollback to.")
    new_id = row[0]
    _update_current(conn, "prompt", new_id)
    _record_rollback(conn, "prompt", current_id, new_id)
    print(f"Rolled back prompt from {current_id} to {new_id}.")


def main():
    parser = argparse.ArgumentParser(description="One‑click rollback utility.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("rollback-model", help="Rollback to previous model version.")
    subparsers.add_parser("rollback-prompt", help="Rollback to previous prompt state.")

    args = parser.parse_args()

    with get_connection() as conn:
        if args.command == "rollback-model":
            rollback_model(conn)
        elif args.command == "rollback-prompt":
            rollback_prompt(conn)
        else:
            parser.error(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()