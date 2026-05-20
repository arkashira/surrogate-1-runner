"""
Shared helpers for the normalization library.
"""

import re
from typing import Callable

# --------------------------------------------------------------------------- #
# Generic whitespace normalizer
# --------------------------------------------------------------------------- #
WHITESPACE_RE = re.compile(r"\s+")

def collapse_whitespace(text: str) -> str:
    """Collapse consecutive whitespace into a single space and strip edges."""
    return WHITESPACE_RE.sub(" ", text).strip()

# --------------------------------------------------------------------------- #
# Generic non‑character remover
# --------------------------------------------------------------------------- #
def remove_non_matching(text: str, pattern: re.Pattern) -> str:
    """Replace anything that does not match the pattern with a single space."""
    return pattern.sub(" ", text)

# --------------------------------------------------------------------------- #
# Dispatcher helper
# --------------------------------------------------------------------------- #
def register_language(name: str, func: Callable[[str], str]) -> None:
    """Register a language‑specific normalizer in the dispatcher."""
    dispatcher = _dispatcher()
    dispatcher[name] = func

def _dispatcher() -> dict:
    """Singleton dispatcher dictionary."""
    if not hasattr(_dispatcher, "_inst"):
        _dispatcher._inst = {}
    return _dispatcher._inst