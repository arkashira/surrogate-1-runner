#!/usr/bin/env python3
"""
Generate Markdown documentation for each workflow template.

Usage:
    python generate_docs.py [--templates DIR] [--docs DIR] [--dry-run]

The script scans the `templates` directory for YAML files that represent
GitHub Actions workflow templates.  For each template it extracts the
`name` and `description` fields (if present) and writes a Markdown file
in the `docs` directory.  An `index.md` file is also generated, listing
all workflows with links to their individual docs.

The script is idempotent: running it multiple times will overwrite the
generated docs with the latest template contents.  The `--dry-run`
option prints what would change without writing any files.
"""

import argparse
import datetime
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def load_yaml(file_path: Path) -> Dict[str, Any]:
    """Load a YAML file safely.  Return an empty dict on parse errors."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as exc:
        print(f"⚠️  Failed to parse {file_path}: {exc}", file=sys.stderr)
        return {}

def sanitize_name(name: str) -> str:
    """Return a safe filename for the workflow name."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name.lower())

def generate_markdown(name: str, description: str, file_path: Path) -> str:
    """Return Markdown content for a workflow."""
    md = f"# {name}\n\n"
    if description:
        md += f"{description}\n\n"
    md += f"**Source file:** `{file_path}`\n\n"
    md += "