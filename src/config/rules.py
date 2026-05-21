"""
Central registry of all supported linting rules.

Each rule is a mapping that must contain at least a ``default_severity`` key.
Additional metadata can be added later without breaking the public API.

The registry is intentionally tiny – it is the single source of truth for
rule names and their default severities.
"""

from __future__ import annotations

from typing import Dict

# --------------------------------------------------------------------------- #
# Rule definitions
# --------------------------------------------------------------------------- #

RULES: Dict[str, Dict[str, str]] = {
    "no-trailing-whitespace": {"default_severity": "warning"},
    "max-line-length": {"default_severity": "error"},
    "no-tabs": {"default_severity": "warning"},
    "indentation": {"default_severity": "error"},
    "unused-import": {"default_severity": "warning"},
    # Add more rules here as the linter evolves.
}

# --------------------------------------------------------------------------- #
# Allowed severity levels
# --------------------------------------------------------------------------- #

SEVERITY_LEVELS = {"error", "warning", "info", "off"}

# --------------------------------------------------------------------------- #
# Convenience helpers (optional, but handy for callers)
# --------------------------------------------------------------------------- #

def is_valid_severity(sev: str) -> bool:
    """Return ``True`` if *sev* is one of the allowed severity levels."""
    return sev in SEVERITY_LEVELS