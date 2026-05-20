"""
Configuration loader for surrogate-1.
Loads baseline signatures from YAML and exposes them via a singleton.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

BASELINE_PATH = Path("/opt/axentx/surrogate-1/config/baseline_signatures.yaml")

def load_baseline_signatures() -> Dict[str, Any]:
    """
    Load baseline signatures from the YAML file.
    Returns an empty dict if the file does not exist or is empty.
    """
    if not BASELINE_PATH.exists():
        return {}
    with BASELINE_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # Expect top-level key 'api_endpoints'
    return data.get("api_endpoints", {})

# Singleton instance to avoid reloading on every request
_BASELINE_CACHE: Dict[str, Any] | None = None

def get_baseline_signatures() -> Dict[str, Any]:
    global _BASELINE_CACHE
    if _BASELINE_CACHE is None:
        _BASELINE_CACHE = load_baseline_signatures()
    return _BASELINE_CACHE