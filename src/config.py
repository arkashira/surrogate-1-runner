"""
Configuration module for the surrogate‑1 rollback system.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any

# Allow overrides via environment variables
CONFIG_FILE = Path(os.getenv("SURROGATE_ROLLBACK_CONFIG", "/opt/axentx/surrogate-1/config/rollback_config.json"))

DEFAULT_CONFIG: Dict[str, Any] = {
    "enabled": True,
    "max_history": 10,
    "rollback_delay_seconds": 5,
    "external_action_endpoint": "https://api.external.com/actions",
    "auth_token": "",
}

logger = logging.getLogger(__name__)


def _atomic_write(path: Path, data: str) -> None:
    """Write *data* to *path* atomically."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(data, encoding="utf-8")
    os.replace(tmp, path)  # atomic on POSIX


def load_config() -> Dict[str, Any]:
    """Load rollback configuration from JSON file.
    If the file does not exist, create it with defaults.
    """
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read config, falling back to defaults: %s", exc)
        return DEFAULT_CONFIG.copy()

    merged = DEFAULT_CONFIG.copy()
    merged.update(data)
    return merged


def save_config(data: Dict[str, Any]) -> None:
    """Persist configuration to disk atomically."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write(CONFIG_FILE, json.dumps(data, indent=2))
    logger.debug("Config written to %s", CONFIG_FILE)


def update_config(updates: Dict[str, Any]) -> None:
    """Update configuration with provided key/value pairs."""
    cfg = load_config()
    cfg.update(updates)
    save_config(cfg)