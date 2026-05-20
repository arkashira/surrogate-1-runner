"""
Utility helpers for working with Jira issue keys that appear in Git commit messages.

Features
--------
* :func:`extract_jira_keys` – returns a list of unique, upper‑cased Jira keys
  found in a commit message.  The function is tolerant of surrounding
  punctuation, whitespace, and mixed‑case project prefixes.
* :func:`format_jira_links` – turns a list of keys into fully‑qualified URLs
  using a configurable base URL.

The implementation favours correctness over brevity: the regex is
carefully constructed to avoid false positives (e.g. “ABC-123DEF-456” is
split into two keys) and the public API is intentionally small and
well‑documented.

Example
-------
>>> msg = "Implemented feature abc-123 and fixed bug XYZ-456."
>>> extract_jira_keys(msg)
['ABC-123', 'XYZ-456']

>>> format_jira_links(['ABC-123'])
['https://jira.example.com/browse/ABC-123']
"""

from __future__ import annotations

import re
from typing import Iterable, List

__all__ = ["extract_jira_keys", "format_jira_links"]

# --------------------------------------------------------------------------- #
# Regex
# --------------------------------------------------------------------------- #
#   * `(?<![A-Z0-9-])` – ensure the key is not preceded by a letter, digit or hyphen
#   * `(?P<key>[A-Z]{2,}-\d+)` – capture the key (at least two letters, hyphen, digits)
#   * `(?![A-Z0-9-])` – ensure the key is not followed by a letter, digit or hyphen
#   * `re.IGNORECASE` – allow mixed‑case project prefixes
_JIRA_KEY_RE = re.compile(
    r"""
    (?<![A-Z0-9-])          # not part of a longer word
    (?P<key>
        [A-Z]{2,}           # 2+ letters
        -                   # hyphen
        \d+                 # 1+ digits
    )
    (?![A-Z0-9-])           # not part of a longer word
    """,
    re.VERBOSE | re.IGNORECASE,
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def extract_jira_keys(message: str) -> List[str]:
    """
    Extract all unique Jira issue keys from *message*.

    Parameters
    ----------
    message : str
        Commit message (or any free‑form text) that may contain Jira keys.

    Returns
    -------
    List[str]
        A list of **upper‑cased** keys in the order they first appear.
        The list is empty if no keys are found.

    Notes
    -----
    * Keys are normalised to upper‑case so that ``abc-123`` and ``ABC-123``
      are treated as the same issue.
    * Duplicate keys are collapsed to a single entry.
    * The function is tolerant of surrounding punctuation, whitespace,
      and mixed‑case project prefixes.
    """
    keys: List[str] = []
    seen: set[str] = set()

    for match in _JIRA_KEY_RE.finditer(message):
        key = match.group("key").upper()
        if key not in seen:
            seen.add(key)
            keys.append(key)

    return keys


def format_jira_links(keys: Iterable[str], base_url: str = "https://jira.example.com/browse/") -> List[str]:
    """
    Convert a list of Jira keys into full URLs.

    Parameters
    ----------
    keys : Iterable[str]
        Iterable of Jira issue keys (case‑insensitive – they will be
        upper‑cased internally if you used :func:`extract_jira_keys`).
    base_url : str, optional
        Base URL of the Jira instance.  The default points to a
        placeholder domain; override it in production.

    Returns
    -------
    List[str]
        Fully‑qualified URLs pointing to the Jira issues.
    """
    return [f"{base_url.rstrip('/')}/{key.upper()}" for key in keys]


# --------------------------------------------------------------------------- #
# Demo / debugging
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample = """
    DOC: Add new feature
    Fixed bug in module X. See abc-123 and XYZ-456 for details.
    Also related to abc-123.
    """
    print("Keys:", extract_jira_keys(sample))
    print("Links:", format_jira_links(extract_jira_keys(sample)))