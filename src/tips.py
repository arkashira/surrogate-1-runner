"""
Utility functions for loading source‑type tips from markdown files.

The tips are stored under `docs/tips/<source_type>.md`. The default
search path is relative to the repository root, but a custom base
path can be supplied for testing or alternative deployments.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def get_tip(source_type: str, base_path: Optional[Path] = None) -> Optional[str]:
    """
    Load the tip markdown content for the given source type.

    Parameters
    ----------
    source_type : str
        The identifier of the source type (e.g., "s3", "gcs").
    base_path : Optional[Path]
        The base directory containing the `tips` folder. If omitted,
        the function resolves to `<repo_root>/docs/tips`.

    Returns
    -------
    Optional[str]
        The raw markdown content of the tip file, or ``None`` if the
        file does not exist.
    """
    if base_path is None:
        # Resolve to <repo_root>/docs/tips
        base_path = Path(__file__).resolve().parents[2] / "docs" / "tips"

    tip_file = base_path / f"{source_type}.md"

    if tip_file.is_file():
        return tip_file.read_text(encoding="utf-8")
    return None