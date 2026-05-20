"""
A tiny, provider‑agnostic wrapper around LLM HTTP APIs.

Features
--------
* Per‑provider API‑key / model configuration stored in a JSON file.
* Lazy, thread‑safe singleton configuration (`CONFIG`).
* Simple `LLMClient(provider).infer(messages)` interface.
* Extensible – add a new provider by extending `_PROVIDER_META`.
* Full type hints and a small, well‑tested public surface.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol

# ----------------------------------------------------------------------
# 1️⃣  Configuration handling
# ----------------------------------------------------------------------


DEFAULT_CONFIG_PATH = Path("/opt/axentx/surrogate-1/config.json")
ENV_CONFIG_PATH = "AXENTX_CONFIG_PATH"


@dataclass
class ProviderConfig:
    """Simple container for a provider's credentials."""

    api_key: str
    model_name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProviderConfig":
        return cls(
            api_key=str(data.get("api_key", "")),
            model_name=str(data.get("model_name", "")),
        )

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


class GlobalConfig:
    """
    Holds the configuration for **all** providers.

    The JSON file looks like: