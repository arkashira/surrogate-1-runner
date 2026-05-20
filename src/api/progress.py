import os
import json
import csv
import io
from datetime import datetime, date
from typing import Dict

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse

# Path to persistent storage (JSON file)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")

router = APIRouter(prefix="/progress", tags=["progress"])


def _load_progress() -> Dict:
    """Load progress data from the JSON file. Return defaults if missing."""
    if not os.path.isfile(PROGRESS_FILE):
        # Default progress structure
        return {
            "total_sessions": 0,
            "terms_learned": 0,
            "total_terms": 0,
            "current_streak": 0,
            "last_practice_date": None,  # ISO string e.g. "2023-01-01"
        }
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        raise HTTPException(status_code=500, detail="Failed to read progress data") from exc


def _save_progress(data: Dict) -> None:
    """Persist progress data to the JSON file."""
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise HTTPException(status_code=500, detail="Failed to write progress data") from exc


def _percentage_learned(learned: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((learned / total) * 100, 2)


@router.get("/", response_model=dict)
def get_progress():
    """
    Return a summary of the user's learning progress.
    """
    data = _load_progress()
    percent = _percentage_learned(data.get("terms_learned", 0), data.get("total_terms", 0))

    # Compute streak based on last practice date
    streak = data.get("current_streak", 0)
    last_date_str = data.get("last_practice_date")
    if last_date_str:
        try:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            today = date.today()
            delta = (today - last_date).days
            if delta == 0:
                # streak is up‑to‑date
                pass
            elif delta == 1:
                # continue streak (already stored)
                pass
            else:
                # break in streak, reset to 0
                streak = 0
        except ValueError:
            # malformed date, ignore streak logic
            pass

    return {
        "total_sessions": data.get("total_sessions", 0),
        "terms_learned_percentage": percent,
        "current_streak": streak,
    }


@router.get("/export", response_class=StreamingResponse)
def export_progress():
    """
    Export the progress data as a CSV file.
    """
    data = _load_progress()
    percent = _percentage_learned(data.get("terms_learned", 0), data.get("total_terms", 0))

    # Prepare CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    # Header
    writer.writerow(
        [
            "date",
            "total_sessions",
            "terms_learned_percentage",
            "current_streak",
        ]
    )
    # Single row with today's date
    writer.writerow(
        [
            date.today().isoformat(),
            data.get("total_sessions", 0),
            percent,
            data.get("current_streak", 0),
        ]
    )
    output.seek(0)

    def iterfile():
        yield output.read()

    headers = {
        "Content-Disposition": f'attachment; filename="progress_{date.today().isoformat()}.csv"'
    }
    return StreamingResponse(iterfile(), media_type="text/csv", headers=headers)