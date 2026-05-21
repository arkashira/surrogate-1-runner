"""
Central configuration loader.
* Environment variables have highest priority.
* `settings.json` is a fallback for bulk defaults.
* All values are typed and validated at import time.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"

# ----------------------------------------------------------------------
# Ensure required directories exist (idempotent)
# ----------------------------------------------------------------------
for p in (DATA_DIR, CACHE_DIR, LOG_DIR):
    p.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# Helper to read the JSON file once (lazy, cached)
# ----------------------------------------------------------------------
_SETTINGS_CACHE: Optional[Dict[str, Any]] = None


def _load_json() -> Dict[str, Any]:
    global _SETTINGS_CACHE
    if _SETTINGS_CACHE is None:
        settings_path = BASE_DIR / "settings.json"
        if settings_path.is_file():
            with settings_path.open("r", encoding="utf-8") as f:
                _SETTINGS_CACHE = json.load(f)
        else:
            _SETTINGS_CACHE = {}
    return _SETTINGS_CACHE


def _get(key: str, default: Any = None) -> Any:
    """Lookup `key` first in env, then in JSON, finally fallback."""
    # Env vars are flat, we support both `PIPELINE_WORKERS` and nested `pipeline.workers`
    env_key = key.upper().replace(".", "_")
    if env_key in os.environ:
        return os.environ[env_key]

    # JSON lookup – support dotted paths
    parts = key.split(".")
    cur = _load_json()
    for part in parts:
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


# ----------------------------------------------------------------------
# Typed, ready‑to‑use settings
# ----------------------------------------------------------------------
PIPELINE_WORKERS: int = int(_get("pipeline.workers", 16))
PIPELINE_INTERVAL_MINUTES: int = int(_get("pipeline.interval_minutes", 30))
PIPELINE_ENABLED: bool = bool(_get("pipeline.enabled", True))

API_TIMEOUT: int = int(_get("api.timeout", 30))
API_RETRY_ATTEMPTS: int = int(_get("api.retry_attempts", 3))
API_RETRY_DELAY: int = int(_get("api.retry_delay", 5))

DATASET_NAME: str = str(_get("dataset.name", "axentx/surrogate-1-training-pairs"))
DATASET_SLUG: str = str(_get("dataset.slug", "reddit"))
SHARD_COUNT: int = int(_get("shard_count", 16))

CACHE_ENABLED: bool = str(_get("cache.enabled", "true")).lower() == "true"
CACHE_TTL_HOURS: int = int(_get("cache.ttl_hours", 24))

LOG_LEVEL: str = str(_get("logging.level", "INFO")).upper()
LOG_FORMAT: str = str(_get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

# ----------------------------------------------------------------------
# Public helpers – useful for tests or dynamic re‑load
# ----------------------------------------------------------------------
def reload_settings() -> None:
    """Force a reload of `settings.json` (useful in long‑running processes)."""
    global _SETTINGS_CACHE
    _SETTINGS_CACHE = None
    _load_json()


def dump_current_settings(path: Path = BASE_DIR / "runtime_settings.json") -> None:
    """Write the *effective* configuration (env + json) to a file for debugging."""
    effective = {
        "pipeline": {
            "workers": PIPELINE_WORKERS,
            "interval_minutes": PIPELINE_INTERVAL_MINUTES,
            "enabled": PIPELINE_ENABLED,
        },
        "api": {
            "timeout": API_TIMEOUT,
            "retry_attempts": API_RETRY_ATTEMPTS,
            "retry_delay": API_RETRY_DELAY,
        },
        "dataset": {
            "name": DATASET_NAME,
            "slug": DATASET_SLUG,
        },
        "cache": {
            "enabled": CACHE_ENABLED,
            "ttl_hours": CACHE_TTL_HOURS,
        },
        "logging": {
            "level": LOG_LEVEL,
            "format": LOG_FORMAT,
        },
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(effective, f, indent=2)