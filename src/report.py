"""
Report module for aggregating and formatting issues discovered during a
single run of the /review feature.

Typical usage
-------------
    from src.report import Report

    report = Report()
    report.add_issue(file="src/foo.py", line=10, message="Unused import")
    report.add_issue(
        file="src/bar.py",
        line=5,
        message="Missing docstring",
        severity="error",
    )
    print(report.render())
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Iterable


# --------------------------------------------------------------------------- #
#  Data model
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class Issue:
    """
    A single issue detected by a scanner.

    Attributes
    ----------
    file : str
        Path to the file where the issue was found.
    line : int
        1‑based line number.
    message : str
        Human‑readable description of the problem.
    severity : str, optional
        One of ``error``, ``warning`` (default), or ``info``.
    """
    file: str
    line: int
    message: str
    severity: str = "warning"

    def to_dict(self) -> Dict[str, str | int]:
        """Return a plain‑dict representation – handy for JSON serialisation."""
        return {
            "file": self.file,
            "line": self.line,
            "message": self.message,
            "severity": self.severity,
        }


# --------------------------------------------------------------------------- #
#  Report collector
# --------------------------------------------------------------------------- #
class Report:
    """
    Collects issues from multiple scanners and renders a single, clear,
    human‑readable report.
    """

    # Order used for deterministic sorting (lower value = higher priority)
    _SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}

    def __init__(self) -> None:
        self._issues: List[Issue] = []

    # --------------------------------------------------------------------- #
    #  Mutating API
    # --------------------------------------------------------------------- #
    def add_issue(
        self,
        *,
        file: str,
        line: int,
        message: str,
        severity: str = "warning",
    ) -> None:
        """
        Add a single issue.

        Parameters
        ----------
        file : str
            Path to the file where the issue was found.
        line : int
            1‑based line number.
        message : str
            Human‑readable description.
        severity : str, optional
            ``error``, ``warning`` (default) or ``info``.
        """
        self._issues.append(
            Issue(file=file, line=line, message=message, severity=severity)
        )

    def extend(self, issues: Iterable[Dict[str, str | int]]) -> None:
        """
        Bulk‑add issues supplied as dictionaries (e.g. from another module).

        Each dict must contain ``file``, ``line`` and ``message`` keys.
        ``severity`` is optional and defaults to ``warning``.
        """
        for raw in issues:
            self.add_issue(
                file=raw["file"],
                line=int(raw["line"]),
                message=raw["message"],
                severity=raw.get("severity", "warning"),
            )

    # --------------------------------------------------------------------- #
    #  Query API
    # --------------------------------------------------------------------- #
    @property
    def issues(self) -> List[Issue]:
        """A shallow copy of the collected issues (read‑only for callers)."""
        return list(self._issues)

    def has_issues(self) -> bool:
        """Return ``True`` if any issues have been recorded."""
        return bool(self._issues)

    # --------------------------------------------------------------------- #
    #  Rendering
    # --------------------------------------------------------------------- #
    def render(self) -> str:
        """
        Produce a formatted, multi‑line string containing all issues.

        Format
        ------
        ``<SEVERITY>: <file>:<line> – <message>``

        The list is sorted by:
        1. severity (error > warning > info)
        2. file name (lexicographically)
        3. line number (numeric)

        Returns
        -------
        str
            Human‑readable report.  If no issues are present a friendly
            “no‑issues” message is returned.
        """
        if not self._issues:
            return "✅ No issues found."

        sorted_issues = sorted(
            self._issues,
            key=lambda i: (
                self._SEVERITY_ORDER.get(i.severity, 99),
                i.file,
                i.line,
            ),
        )

        lines = [
            f"{i.severity.upper()}: {i.file}:{i.line} – {i.message}"
            for i in sorted_issues
        ]

        header = f"🛑 {len(self._issues)} issue{'s' if len(self._issues) != 1 else ''} found:"
        return "\n".join([header] + lines)