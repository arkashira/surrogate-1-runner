"""
Git hook parser for DOC: commits.

The module extracts the article body from a commit message that starts
with the `DOC:` prefix (case‑insensitive) and returns any Jira issue
keys that appear in the message.  It is designed to be imported by a
Git hook script that runs on commit or push events.

Author: axentx-dev-bot
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

# --------------------------------------------------------------------------- #
# Regular expressions
# --------------------------------------------------------------------------- #

# Matches Jira keys such as ABC-123, PROJ-456, etc.
JIRA_KEY_RE: re.Pattern[str] = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")

# Matches the DOC: prefix, case‑insensitive, allowing leading whitespace.
DOC_PREFIX_RE: re.Pattern[str] = re.compile(r"^\s*DOC:\s*", re.IGNORECASE)


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _unique_keys(keys: List[str]) -> List[str]:
    """
    Return a list of unique strings preserving the original order.

    Parameters
    ----------
    keys : List[str]
        The list of keys to deduplicate.

    Returns
    -------
    List[str]
        The deduplicated list.
    """
    return list(dict.fromkeys(keys))


def extract_jira_keys(message: str) -> List[str]:
    """
    Extract all unique Jira issue keys from a commit message.

    Parameters
    ----------
    message : str
        The full commit message.

    Returns
    -------
    List[str]
        A list of unique Jira keys in the order they appear.
    """
    return _unique_keys(JIRA_KEY_RE.findall(message))


def extract_doc_content(message: str) -> Optional[str]:
    """
    Extract the article body from a DOC: commit message.

    Parameters
    ----------
    message : str
        The full commit message.

    Returns
    -------
    Optional[str]
        The article body (first line without the DOC: prefix plus any
        subsequent lines), or ``None`` if the message does not start
        with the DOC: prefix.
    """
    lines = message.splitlines()
    if not lines:
        return None

    first_line = lines[0]
    if not DOC_PREFIX_RE.match(first_line):
        return None

    # Remove the DOC: prefix from the first line
    content_lines = [DOC_PREFIX_RE.sub("", first_line, count=1)]
    # Append the rest of the lines unchanged
    content_lines.extend(lines[1:])

    article = "\n".join(content_lines).strip()
    return article or None


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def parse_commit(message: str) -> Optional[Tuple[str, List[str]]]:
    """
    Parse a commit message for DOC: content and Jira keys.

    Parameters
    ----------
    message : str
        The full commit message.

    Returns
    -------
    Optional[Tuple[str, List[str]]]
        ``(article_content, jira_keys)`` if the message starts with
        ``DOC:``; otherwise ``None``.
    """
    content = extract_doc_content(message)
    if content is None:
        return None

    keys = extract_jira_keys(message)
    return content, keys


# --------------------------------------------------------------------------- #
# Demo / CLI
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample = """DOC: Add new authentication flow
This commit introduces a new OAuth2 flow for the API.
It includes updated client libraries and documentation.

Related issues: AX-123, AX-456
"""
    result = parse_commit(sample)
    if result:
        article, keys = result
        print("Article content:")
        print(article)
        print("\nLinked Jira keys:", keys)
    else:
        print("Not a DOC: commit.")