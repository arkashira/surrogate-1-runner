"""
Utility to load per‑user configuration.

Configuration files live in `configs/<user_id>.json` and must contain a
`target_language` key.  The module falls back to English (`EN`) if the file
is missing or malformed.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

CONFIG_DIR = Path("configs")

def load_user_config(user_id: str) -> Dict[str, str]:
    """Return a dict with at least a `target_language` key."""
    path = CONFIG_DIR / f"{user_id}.json"
    if not path.is_file():
        logger.warning("Missing config for user %s – defaulting to EN", user_id)
        return {"target_language": "EN"}

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if "target_language" not in data:
                raise KeyError
            return data
    except (json.JSONDecodeError, KeyError) as exc:
        logger.error("Invalid config for user %s: %s", user_id, exc)
        return {"target_language": "EN"}