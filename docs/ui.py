"""
Surrogate‑1 Documentation UI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a Flask blueprint that renders the project's Markdown
documentation and offers a very small keyword search.

The implementation is intentionally lightweight – it loads the
`docs.md` file on every request so the UI always reflects the
latest changes.  No background file‑watcher is required.

Author:  AI‑Synthesiser
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict, Any

from flask import (
    Blueprint,
    render_template_string,
    request,
    jsonify,
    current_app,
)

# --------------------------------------------------------------------------- #
# Blueprint definition
# --------------------------------------------------------------------------- #

docs_bp = Blueprint("docs", __name__, url_prefix="/docs")

# --------------------------------------------------------------------------- #
# Helpers – Markdown rendering
# --------------------------------------------------------------------------- #

def _load_markdown() -> str:
    """
    Load the Markdown file that lives next to this module and
    convert it to HTML.

    Returns
    -------
    str
        Rendered HTML or a fallback message if the file is missing.
    """
    md_path = Path(__file__).with_name("docs.md")
    if not md_path.is_file():
        return "<p><em>No documentation available.</em></p>"

    md_text = md_path.read_text(encoding="utf-8")

    try:
        import markdown  # type: ignore
        # Use fenced code blocks and tables – the most common extensions.
        html = markdown.markdown(md_text, extensions=["fenced_code", "tables"])
    except Exception:  # pragma: no cover
        # If the markdown library is missing, fall back to a pre‑formatted block.
        html = f"<pre>{md_text}</pre>"

    return html


# --------------------------------------------------------------------------- #
# Helpers – Search
# --------------------------------------------------------------------------- #

def _search_markdown(query: str) -> List[Dict[str, Any]]:
    """
    Very small, case‑insensitive keyword search that scans the raw
    Markdown file line by line.

    Parameters
    ----------
    query : str
        The search string.

    Returns
    -------
    List[Dict[str, Any]]
        Each dict contains:
        - line (int): 1‑based line number.
        - snippet (str): 5‑line context around the match.
    """
    if not query:
        return []

    md_path = Path(__file__).with_name("docs.md")
    if not md_path.is_file():
        return []

    lines = md_path.read_text(encoding="utf-8").splitlines()
    results: List[Dict[str, Any]] = []

    q = query.lower()
    for idx, line in enumerate(lines):
        if q in line.lower():
            # 2 lines before + 3 lines after (or as many as exist)
            start = max(0, idx - 2)
            end = min(len(lines), idx + 3)
            snippet = "\n".join(lines[start:end]).strip()
            results.append({"line": idx + 1, "snippet": snippet})

    return results


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #

@docs_bp.route("/", methods=["GET"])
def docs_page() -> str:
    """
    Render the documentation page.

    The template contains a placeholder `{{ content }}` that is
    replaced with the rendered Markdown.
    """
    content_html = _load_markdown()
    template = _load_template()
    return render_template_string(template, content=content_html)


@docs_bp.route("/search", methods=["GET"])
def search() -> Any:
    """
    API endpoint for keyword search.

    Query parameters
    ----------------
    q : str
        The search string.

    Returns
    -------
    JSON
        {"results": [...]} – see `_search_markdown` for the shape.
    """
    query = request.args.get("q", "").strip()
    results = _search_markdown(query)
    return jsonify(results=results)


# --------------------------------------------------------------------------- #
# Template loader
# --------------------------------------------------------------------------- #

def _load_template() -> str:
    """
    Load the static HTML template that lives next to this module.
    The template is tiny and contains the search UI, result list
    and a placeholder for the rendered Markdown.
    """
    tmpl_path = Path(__file__).with_name("docs.html")
    return tmpl_path.read_text(encoding="utf-8")