"""
Utility for generating a concise headline summarizing the overall
status of a daily digest.

The headline can be produced from two different sources:

* A list of raw items (each item is a mapping that must contain a
  ``content`` key).  The class will count incidents and deployments
  using regex patterns.
* A pre‑aggregated ``stats`` dictionary that may contain the keys
  ``incidents``, ``deployments``, ``alerts`` and ``downtime``.

The headline follows the same rules as in Candidate 2, but the
incident/deployment counts are derived automatically when only items
are provided.
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Mapping, Sequence, Union

# --------------------------------------------------------------------------- #
# Helper – pluralisation
# --------------------------------------------------------------------------- #
def _pluralize(count: int, singular: str, plural: str | None = None) -> str:
    """Return a string with the count and the appropriate singular/plural form."""
    if plural is None:
        plural = singular + "s"
    return f"{count} {singular if count == 1 else plural}"


# --------------------------------------------------------------------------- #
# HeadlineGenerator
# --------------------------------------------------------------------------- #
class HeadlineGenerator:
    """
    Generate a headline from either raw items or a stats dictionary.

    Parameters
    ----------
    items : Iterable[Mapping[str, str]] | None
        Raw items that contain a ``content`` key.  If supplied, the
        generator will count incidents and deployments using regex.
    stats : Mapping[str, int | bool] | None
        Pre‑aggregated statistics.  If supplied, it overrides any
        counts derived from ``items``.
    """

    # Regex patterns – copied from Candidate 1
    _INCIDENT_RE = re.compile(r"incident|outage|failure|error", re.IGNORECASE)
    _DEPLOY_RE = re.compile(r"deploy|release|update|rollout", re.IGNORECASE)

    def __init__(
        self,
        items: Iterable[Mapping[str, str]] | None = None,
        stats: Mapping[str, int | bool] | None = None,
    ) -> None:
        self.items = list(items) if items is not None else []
        self.stats = dict(stats) if stats is not None else {}

    # ----------------------------------------------------------------------- #
    # Counting helpers
    # ----------------------------------------------------------------------- #
    def _count_incidents(self) -> int:
        return sum(1 for it in self.items if self._INCIDENT_RE.search(it.get("content", "")))

    def _count_deployments(self) -> int:
        return sum(1 for it in self.items if self._DEPLOY_RE.search(it.get("content", "")))

    # ----------------------------------------------------------------------- #
    # Public API
    # ----------------------------------------------------------------------- #
    def generate(self) -> str:
        """
        Return a headline string.

        The method first looks for ``incidents`` and ``deployments`` in
        ``self.stats``.  If they are missing, it falls back to counting
        them from ``self.items``.  The optional ``alerts`` and
        ``downtime`` values are taken from ``self.stats`` if present.
        """
        # Pull counts from stats if available, otherwise count from items
        incidents = int(self.stats.get("incidents", self._count_incidents()))
        deployments = int(self.stats.get("deployments", self._count_deployments()))
        alerts = int(self.stats.get("alerts", 0))
        downtime = bool(self.stats.get("downtime", False))

        parts: List[str] = []

        # Incident part
        if incidents:
            parts.append(_pluralize(incidents, "incident"))
        else:
            parts.append("No incidents")

        # Deployments part
        parts.append(f"{_pluralize(deployments, 'deployment')} scheduled")

        # Optional downtime
        if downtime:
            parts.append("and downtime")

        # Optional alerts
        if alerts:
            parts.append(f"and {_pluralize(alerts, 'alert')}")

        return ", ".join(parts)