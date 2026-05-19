"""
HTML formatter for coverage data.

The formatter turns raw coverage information into a table
with visual indicators for uncovered lines.  Uncovered lines
are highlighted in red to make gaps obvious.

The function is intentionally pure and side‑effect free,
making it easy to unit‑test.
"""

from __future__ import annotations

from typing import Dict, Iterable, Set

def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )

def format_coverage_html(
    coverage_data: Dict[str, Dict[str, Iterable[int] | Set[int]]]
) -> str:
    """
    Convert coverage data into an HTML table.

    Parameters
    ----------
    coverage_data:
        Mapping from file paths to coverage information.

    Returns
    -------
    str
        HTML fragment containing a table per file.
    """
    fragments: list[str] = []

    for file_path, data in sorted(coverage_data.items()):
        lines: Iterable[int] = data.get("lines", [])
        executed: Set[int] = set(data.get("executed", []))

        # Header for the file
        fragments.append(f"<h2>{_escape_html(file_path)}</h2>")
        fragments.append("<table>")
        fragments.append("<tr><th>Line</th><th>Code</th></tr>")

        # Read the source file once
        try:
            source = open(file_path, encoding="utf-8").read().splitlines()
        except Exception:
            source = ["<Unable to read file>"]

        for line_no in sorted(lines):
            code = source[line_no - 1] if 0 <= line_no - 1 < len(source) else ""
            css = "uncovered" if line_no not in executed else ""
            fragments.append(
                f"<tr class='{css}'><td>{line_no}</td><td>{_escape_html(code)}</td></tr>"
            )

        fragments.append("</table>")

    return "\n".join(fragments)