"""
Centralised configuration for the surrogate‑1 application.

* Loads a JSON configuration file (`config.json`) that contains
  broker URLs, result backends, and optional overrides.
* Loads a JSON *schema* (`finance_schema.json`) that tells the
  job which columns in the raw CSVs represent revenue and expense.
* Exposes absolute paths for raw data and metrics output.
"""

from __future__ import annotations

import json
import pathlib
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Base directories
# --------------------------------------------------------------------------- #
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "finance"
RAW_DIR = DATA_DIR / "raw"
METRICS_DIR = DATA_DIR / "metrics"

# Ensure the metrics directory exists – Celery will write to it.
METRICS_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
# Configuration files
# --------------------------------------------------------------------------- #
CONFIG_PATH = BASE_DIR / "config.json"
SCHEMA_PATH = BASE_DIR / "config" / "finance_schema.json"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _load_json(path: pathlib.Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
# Load the main config – this is the only place that raises if the file is missing.
CONFIG: Dict[str, Any] = _load_json(CONFIG_PATH)

# Load the finance schema – this is optional; if missing we default to common names.
try:
    SCHEMA: Dict[str, str] = _load_json(SCHEMA_PATH)
except FileNotFoundError:
    SCHEMA = {"revenue": "revenue", "expense": "expense"}

# Convenience aliases used throughout the codebase
BROKER_URL = CONFIG["celery"]["broker_url"]
RESULT_BACKEND = CONFIG["celery"]["result_backend"]