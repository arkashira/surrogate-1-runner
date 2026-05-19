"""
Refresh‑rate configuration for Surrogate‑1.

* Validates that the chosen refresh rate is a positive integer ≤ 240 Hz.
* Persists the setting to a JSON file (default: ./config/ui_settings.json).
* Allows the config path to be overridden with the SURROGATE_UI_SETTINGS env‑var.
* Provides a tiny Tkinter UI that works with the same model.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

# ----------------------------------------------------------------------
# 1️⃣  Constants & validation
# ----------------------------------------------------------------------
_MAX_REFRESH_RATE_HZ = 240
_SUPPORTED_RATES: List[int] = [30, 60, 120, 144, 165, 240]  # friendly drop‑down values


def _validate_refresh_rate(value: int) -> int:
    """Clamp and validate a refresh‑rate value.

    Args:
        value: Desired refresh rate in Hz.

    Returns:
        An integer in the range 1 … _MAX_REFRESH_RATE_HZ.

    Raises:
        ValueError: If ``value`` is not a positive integer.
    """
    if not isinstance(value, int) or value <= 0:
        raise ValueError("Refresh rate must be a positive integer")
    # Clamp to the hardware limit – we never store a value > 240.
    return min(value, _MAX_REFRESH_RATE_HZ)


# ----------------------------------------------------------------------
# 2️⃣  Dataclass that always holds a validated value
# ----------------------------------------------------------------------
@dataclass
class UISettings:
    """Container for UI‑related configuration."""

    refresh_rate_hz: int = field(
        default=60,
        metadata={"description": "Display refresh rate in Hz"},
    )

    def __post_init__(self) -> None:
        # Guarantees the instance is always valid, even when constructed
        # from raw JSON data.
        self.refresh_rate_hz = _validate_refresh_rate(self.refresh_rate_hz)


# ----------------------------------------------------------------------
# 3️⃣  Load / save helpers (JSON, env‑var, safe defaults)
# ----------------------------------------------------------------------
def _resolve_path(explicit: str | None) -> Path:
    """Return the absolute path that should be used for the config file."""
    if explicit:
        return Path(explicit).expanduser().resolve()
    env_path = os.getenv("SURROGATE_UI_SETTINGS")
    if env_path:
        return Path(env_path).expanduser().resolve()
    # Default location – keep it inside the project tree.
    return Path("./config/ui_settings.json").expanduser().resolve()


def load_settings_from_file(path: str | None = None) -> UISettings:
    """Load UI settings from a JSON file.

    If the file does not exist, is malformed, or contains invalid data,
    a **default** :class:`UISettings` instance is returned so the UI stays
    functional.
    """
    cfg_path = _resolve_path(path)

    try:
        with cfg_path.open("r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
        # ``int(...)`` will raise if the value is not numeric – caught below.
        return UISettings(refresh_rate_hz=int(data.get("refresh_rate_hz", 60)))
    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError):
        # Any problem falls back to safe defaults.
        return UISettings()


def save_settings_to_file(settings: UISettings, path: str | None = None) -> None:
    """Persist a :class:`UISettings` instance to JSON."""
    cfg_path = _resolve_path(path)
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    with cfg_path.open("w", encoding="utf-8") as f:
        json.dump({"refresh_rate_hz": settings.refresh_rate_hz}, f, indent=2)


# ----------------------------------------------------------------------
# 4️⃣  Helper for headless/front‑end frameworks (e.g. React, Qt)
# ----------------------------------------------------------------------
def render_settings_ui(current: UISettings) -> Dict[str, Any]:
    """
    Return a serialisable description of the settings UI.

    Front‑ends can consume this dict to build a form without hard‑coding
    the field layout.
    """
    return {
        "fields": [
            {
                "name": "refresh_rate_hz",
                "label": "Refresh Rate (Hz)",
                "type": "number",
                "value": current.refresh_rate_hz,
                "min": 1,
                "max": _MAX_REFRESH_RATE_HZ,
                "step": 1,
                "description": "Set the display refresh rate. Values above 240 Hz are capped.",
            }
        ],
        "submit_endpoint": "/api/settings/update",
    }