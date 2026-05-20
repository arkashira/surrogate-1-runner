"""
Logging module for surrogate-1.

Provides a thread‑safe logger that records AI model access events with
timestamps and user details. Logs are written as JSON lines to a
secure file and can be exported to CSV or JSON format for audits.
"""

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Default log file path relative to the project root
_LOG_DIR = Path(__file__).resolve().parent / "logs"
_LOG_FILE = _LOG_DIR / "access.log"

# Ensure log directory exists with restrictive permissions
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_LOG_FILE.touch(exist_ok=True)
# Set file permissions to read/write for owner only (600)
os.chmod(_LOG_FILE, 0o600)

# Thread‑safety lock for file writes
_lock = threading.Lock()


def _current_timestamp() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.utcnow().isoformat() + "Z"


def log_access(user_id: str, action: str, details: Optional[Dict] = None) -> None:
    """
    Log an access event.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action (e.g., "model_inference").
    details : dict, optional
        Additional context for the event.

    The log entry is written as a JSON line to the log file with the
    following structure:
        {
            "timestamp": "<ISO8601 UTC>",
            "user_id": "<user_id>",
            "action": "<action>",
            "details": { ... }
        }
    """
    entry: Dict = {
        "timestamp": _current_timestamp(),
        "user_id": user_id,
        "action": action,
        "details": details or {},
    }

    line = json.dumps(entry, ensure_ascii=False)

    with _lock:
        with _LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def export_logs_csv(output_path: Path) -> None:
    """
    Export all log entries to a CSV file.

    Parameters
    ----------
    output_path : Path
        Destination file path for the CSV output.
    """
    import csv

    with _lock:
        with _LOG_FILE.open("r", encoding="utf-8") as f:
            reader = (json.loads(line) for line in f if line.strip())

            # Determine CSV headers
            headers = ["timestamp", "user_id", "action", "details"]
            with output_path.open("w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for entry in reader:
                    # Convert details dict to JSON string for CSV
                    entry_copy = entry.copy()
                    entry_copy["details"] = json.dumps(entry_copy["details"], ensure_ascii=False)
                    writer.writerow(entry_copy)


def export_logs_json(output_path: Path) -> None:
    """
    Export all log entries to a single JSON array file.

    Parameters
    ----------
    output_path : Path
        Destination file path for the JSON output.
    """
    with _lock:
        with _LOG_FILE.open("r", encoding="utf-8") as f:
            entries: List[Dict] = [json.loads(line) for line in f if line.strip()]

        with output_path.open("w", encoding="utf-8") as out:
            json.dump(entries, out, ensure_ascii=False, indent=2)


def read_logs() -> List[Dict]:
    """
    Return all log entries as a list of dictionaries.

    Useful for unit tests or in‑memory inspection.
    """
    with _lock:
        with _LOG_FILE.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]


# If this module is executed directly, demonstrate a simple log entry
if __name__ == "__main__":
    log_access("admin@example.com", "model_inference", {"model": "gpt-4", "prompt_length": 42})
    print(f"Logged entry. Current log count: {len(read_logs())}")