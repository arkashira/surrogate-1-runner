"""
A tiny, pure‑Python library that implements a file‑based versioning system
for JSON configuration files.

The public API is intentionally small so it can be reused in CI scripts,
web services, or other tooling.

Author:  Axentx (2026‑05‑14)
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Dict, List, Optional

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

BASE_DIR: pathlib.Path = pathlib.Path(
    pathlib.Path(__file__).resolve().parent.parent / "test_configurations_versions"
)

# --------------------------------------------------------------------------- #
# Internal helpers
# --------------------------------------------------------------------------- #

def _ensure_base_dir() -> None:
    """Create the base directory if it does not exist."""
    BASE_DIR.mkdir(parents=True, exist_ok=True)


_VERSION_RE = re.compile(r"^v(?P<num>\d{3})$")

def _validate_version_id(v: str) -> None:
    """Raise ValueError if *v* is not of the form 'vNNN'."""
    if not _VERSION_RE.match(v):
        raise ValueError(
            f"Invalid version identifier '{v}'. "
            "Must be of the form 'vNNN' where NNN is a three‑digit number."
        )


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def list_versions() -> List[str]:
    """
    Return a sorted list of available version identifiers.

    Example: ["v001", "v002", "v010"]
    """
    _ensure_base_dir()
    return sorted(
        f.stem for f in BASE_DIR.glob("v*.json") if _VERSION_RE.match(f.stem)
    )


def get_latest_version() -> Optional[str]:
    """
    Return the most recent version identifier, or None if no versions exist.
    """
    versions = list_versions()
    return versions[-1] if versions else None


def get_config(version: Optional[str] = None) -> Dict:
    """
    Load and return the configuration dictionary for the given version.

    If *version* is None, the latest version is used.
    Raises FileNotFoundError if the requested version does not exist.
    """
    _ensure_base_dir()
    if version is None:
        version = get_latest_version()
        if version is None:
            raise FileNotFoundError("No test configuration versions are available.")

    _validate_version_id(version)
    config_path = BASE_DIR / f"{version}.json"

    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise ConfigurationError(
            f"Configuration file {config_path} contains invalid JSON."
        ) from exc
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Configuration {version} does not exist.") from exc


def save_config(version: str, config: Dict) -> None:
    """
    Persist a configuration dict under the given version identifier.
    Overwrites any existing file with the same version.
    """
    _validate_version_id(version)
    _ensure_base_dir()
    config_path = BASE_DIR / f"{version}.json"

    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, sort_keys=True)


def bump_version() -> str:
    """
    Generate the next version identifier based on the latest existing version.
    Returns the new version string (e.g., "v002").
    """
    latest = get_latest_version()
    if latest is None:
        return "v001"
    num = int(latest.lstrip("v"))
    return f"v{num + 1:03d}"


# --------------------------------------------------------------------------- #
# Custom exception types
# --------------------------------------------------------------------------- #

class ConfigurationError(RuntimeError):
    """Raised when a configuration file cannot be parsed or is otherwise invalid."""