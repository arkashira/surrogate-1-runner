"""
Thai text normalization pipeline.

Keeps the original logic from Candidate 2 but cleans up the
implementation and adds a small amount of Unicode‑aware punctuation
handling.
"""

import re
from ._common import collapse_whitespace, remove_non_matching, register_language

# --------------------------------------------------------------------------- #
# Regular expressions
# --------------------------------------------------------------------------- #
# Keep Thai block, digits, and ASCII alphanumerics
THAI_ALLOWED_RE = re.compile(r"[^\u0E00-\u0E7F0-9A-Za-z]+")

# Thai punctuation that should be preserved (e.g. ฿, ็, ฯ)
THAI_PUNCTUATION = r"[\u0E3F\u0E4F\u0E5A\u0E5B\u0E5C\u0E5D\u0E5E\u0E5F]"

# --------------------------------------------------------------------------- #
# Normalization steps
# --------------------------------------------------------------------------- #
def _strip_non_thai(text: str) -> str:
    """Remove any non‑Thai characters except alphanumerics."""
    return remove_non_matching(text, THAI_ALLOWED_RE)

def _remove_duplicate_punctuation(text: str) -> str:
    """Replace sequences of the same Thai punctuation with a single instance."""
    pattern = re.compile(r"({0})\1+".format(THAI_PUNCTUATION))
    return pattern.sub(r"\1", text)

def normalize(text: str) -> str:
    """Public API – normalize Thai text."""
    if not text:
        return ""

    text = _strip_non_thai(text)
    text = collapse_whitespace(text)
    text = _remove_duplicate_punctuation(text)
    return text

# --------------------------------------------------------------------------- #
# Register in dispatcher
# --------------------------------------------------------------------------- #
register_language("th", normalize)
register_language("thai", normalize)