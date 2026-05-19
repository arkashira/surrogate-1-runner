from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiagnosticOutput:
    resource_usage: Optional[str] = None
    logs: Optional[str] = None
    config_diff: Optional[str] = None


@dataclass
class Alert:
    message: str
    action_links: List[dict]  # e.g. [{"url": "...", "text": "..."}]