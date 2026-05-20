"""
Severity classification helper.

This module provides a simple mapping from an integer impact score to a
severity label (Low, Medium, High).  The mapping is defined by an
`IMPACT_MATRIX` that can be adjusted to match the organization's
impact matrix.

Functions
---------
classify_severity(impact: int) -> str
    Return the severity label for the given impact score.

is_high_severity(impact: int) -> bool
    Convenience wrapper that returns ``True`` if the impact is classified
    as ``High``.
"""

from __future__ import annotations

__all__ = ["IMPACT_MATRIX", "classify_severity", "is_high_severity"]

# Define the impact ranges for each severity level.
# These ranges are inclusive of the lower bound and exclusive of the upper bound.
IMPACT_MATRIX = {
    "Low": range(0, 4),     # 0-3
    "Medium": range(4, 8),  # 4-7
    "High": range(8, 11),   # 8-10
}


def classify_severity(impact: int) -> str:
    """
    Classify an integer impact score into a severity label.

    Parameters
    ----------
    impact : int
        The numeric impact score of a violation.

    Returns
    -------
    str
        One of ``"Low"``, ``"Medium"``, or ``"High"``.

    Raises
    ------
    ValueError
        If ``impact`` is negative or does not fall within any defined range.
    """
    if impact < 0:
        raise ValueError(f"Impact score must be non‑negative, got {impact}")

    for severity, rng in IMPACT_MATRIX.items():
        if impact in rng:
            return severity

    # If we get here, the impact is outside the defined ranges.
    raise ValueError(
        f"Impact score {impact} is outside the defined severity ranges: {IMPACT_MATRIX}"
    )


def is_high_severity(impact: int) -> bool:
    """
    Return ``True`` if the impact score is classified as ``High``.

    Parameters
    ----------
    impact : int
        The numeric impact score of a violation.

    Returns
    -------
    bool
        ``True`` if ``classify_severity(impact) == "High"``, otherwise ``False``.
    """
    return classify_severity(impact) == "High"