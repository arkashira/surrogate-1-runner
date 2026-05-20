"""
Simple template definitions for cost reports.

The PDF report uses a Jinja2 template to render the header and table
contents. The CSV report is generated directly from the data list.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

# Jinja2 is used only for rendering the PDF header and table rows.
# The actual PDF generation is handled by reportlab.
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    Environment = None  # type: ignore
    FileSystemLoader = None  # type: ignore
    select_autoescape = None  # type: ignore

# Path to the templates directory relative to this file
TEMPLATE_DIR = Path(__file__).parent / "templates"

# Ensure the templates directory exists
TEMPLATE_DIR.mkdir(exist_ok=True)

# Create a minimal header template
HEADER_TEMPLATE = """
Cost Report
===========

Generated on: {{ generated_on }}

"""

# Create a minimal table template
TABLE_TEMPLATE = """
{% for row in rows %}
{{ row.project:<20 }} {{ row.team:<15 }} {{ row.cost:>10.2f }} {{ row.date }}
{% endfor %}
"""

# Write templates to files if they don't exist
if not (TEMPLATE_DIR / "header.txt").exists():
    (TEMPLATE_DIR / "header.txt").write_text(HEADER_TEMPLATE.strip())
if not (TEMPLATE_DIR / "table.txt").exists():
    (TEMPLATE_DIR / "table.txt").write_text(TABLE_TEMPLATE.strip())

# Load templates using Jinja2
env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape()
)

header_template = env.get_template("header.txt")
table_template = env.get_template("table.txt")


def render_header(generated_on: str) -> str:
    """Render the header section."""
    return header_template.render(generated_on=generated_on)


def render_table(rows: List[Dict[str, Any]]) -> str:
    """Render the table section."""
    return table_template.render(rows=rows)