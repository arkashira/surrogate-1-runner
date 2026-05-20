"""
Simple data processor for compliance deadlines.
Expects a CSV file with columns:
    name,date,description
Where `date` is in ISO format YYYY-MM-DD.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, NamedTuple

class Deadline(NamedTuple):
    name: str
    date: datetime
    description: str

def load_deadlines(csv_path: Path) -> List[Deadline]:
    """
    Load deadlines from a CSV file.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        List of Deadline objects.
    """
    deadlines: List[Deadline] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row["date"], "%Y-%m-%d").date()
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Invalid row in {csv_path}: {row}") from exc
            deadlines.append(Deadline(
                name=row.get("name", "Unnamed Deadline"),
                date=date,
                description=row.get("description", ""),
            ))
    return deadlines