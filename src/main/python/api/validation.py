"""
Utility functions for validating uploaded CSV files for finance transactions.
"""

import csv
import io
from datetime import datetime
from typing import List, Tuple, Dict, Any

# Expected CSV headers – order matters for csv.DictReader
EXPECTED_HEADERS = [
    "transaction_id",
    "date",
    "amount",
    "currency",
    "description",
    "merchant",
]

def _parse_date(value: str) -> bool:
    """Return True if value matches YYYY‑MM‑DD, else False."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def _parse_amount(value: str) -> bool:
    """Return True if value can be cast to float, else False."""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

def validate_csv_content(file_stream: io.BytesIO) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Validate the CSV content.

    Parameters
    ----------
    file_stream : io.BytesIO
        The in‑memory file stream of the uploaded CSV.

    Returns
    -------
    Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]
        * A list of valid rows as dictionaries.
        * A list of error dictionaries with row number and error message.
    """
    valid_rows: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    # Reset stream position to the beginning
    file_stream.seek(0)
    decoded = io.TextIOWrapper(file_stream, encoding="utf-8")
    reader = csv.DictReader(decoded)

    # Header validation
    if reader.fieldnames != EXPECTED_HEADERS:
        errors.append(
            {
                "row": 0,
                "error": f"Invalid headers. Expected {EXPECTED_HEADERS}, got {reader.fieldnames}",
            }
        )
        return valid_rows, errors

    for row_num, row in enumerate(reader, start=2):  # start=2 accounts for header row
        row_errors: List[str] = []

        # Required field presence
        for field in EXPECTED_HEADERS:
            if not row.get(field):
                row_errors.append(f"Missing field '{field}'")

        # Date format
        if not _parse_date(row.get("date", "")):
            row_errors.append("Invalid date format, expected YYYY-MM-DD")

        # Amount numeric
        if not _parse_amount(row.get("amount", "")):
            row_errors.append("Amount must be a number")

        if row_errors:
            errors.append({"row": row_num, "error": "; ".join(row_errors)})
        else:
            valid_rows.append(row)

    return valid_rows, errors