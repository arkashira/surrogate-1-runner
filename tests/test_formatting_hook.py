"""
A single, self‑contained test suite that validates the formatting hook.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import textwrap
import tempfile
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# 1️⃣  Fixtures – one per file type (bad / good) and one repo helper
# --------------------------------------------------------------------------- #

@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Return a fresh, empty git‑style repository."""
    r = tmp_path / "repo"
    r.mkdir()
    (r / ".git").mkdir()
    return r


@pytest.fixture
def pre_commit_config(tmp_path: Path) -> Path:
    """Create a minimal .pre‑commit‑config.yaml that excludes a fixture dir."""
    cfg = textwrap.dedent(
        """
        repos:
          - repo: local
            hooks:
              - id: format-check
                name: Format Checker
                entry: python -m formatting_hook
                language: system
                types: [python, markdown, json]
                exclude: '^tests/fixtures/.*$'
        """
    )
    p = tmp_path / ".pre-commit-config.yaml"
    p.write_text(cfg)
    return p


@pytest.fixture
def bad_python(repo: Path) -> Path:
    p = repo / "bad.py"
    p.write_text(
        textwrap.dedent(
            """
            def  bad_function(  ):
                x=1
                y = 2
                z=3
                return x+y+z
            """
        )
    )
    return p


@pytest.fixture
def good_python(repo: Path) -> Path:
    p = repo / "good.py"
    p.write_text(
        textwrap.dedent(
            """
            def good_function():
                """\"\"\"A well‑formatted function.\"\"\""""
                x = 1
                y = 2
                z = 3
                return x + y + z
            """
        )
    )
    return p


@pytest.fixture
def bad_markdown(repo: Path) -> Path:
    p = repo / "bad.md"
    p.write_text(
        textwrap.dedent(
            """
            # Bad Markdown

            This line is way too long and should trigger a line‑length warning from markdownlint because it exceeds the recommended 80 character limit for readability and consistency across the codebase.

            * List item 1
            *List item 2 (missing space)