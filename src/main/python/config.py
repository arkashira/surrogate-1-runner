"""
Centralised configuration for the Finance Ingest service.
"""

import os
from pathlib import Path
from datetime import date
from typing import Set

# ------------------------------------------------------------------
# 1️⃣  Directories
# ------------------------------------------------------------------
BASE_RAW_DIR: Path = Path(os.getenv("BASE_RAW_DIR", "/data/finance/raw"))
BASE_RAW_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# 2️⃣  Celery
# ------------------------------------------------------------------
CELERY_BROKER_URL: str = os.getenv(
    "CELERY_BROKER_URL", "redis://localhost:6379/0"
)
CELERY_RESULT_BACKEND: str = os.getenv(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)

# ------------------------------------------------------------------
# 3️⃣  Upload limits
# ------------------------------------------------------------------
MAX_UPLOAD_SIZE_BYTES: int = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", 10 * 1024 * 1024))
ALLOWED_MIME_TYPES: Set[str] = {
    "text/csv",
    "application/vnd.ms-excel",
    "text/plain",  # some clients send plain text for CSV
}

# ------------------------------------------------------------------
# 4️⃣  Logging
# ------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# ------------------------------------------------------------------
# 5️⃣  Helpers
# ------------------------------------------------------------------
def today_str() -> str:
    """Return YYYY‑MM‑DD for the current day."""
    return date.today().isoformat()