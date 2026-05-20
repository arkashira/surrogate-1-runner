"""
Utility helpers to inspect the current codebase.
"""

import os
from pathlib import Path
from typing import List


def list_py_files(root: str = "/opt/axentx/surrogate-1") -> List[str]:
    """Return a list of all .py files under *root*."""
    return [
        str(p)
        for p in Path(root).rglob("*.py")
        if p.is_file()
    ]


def show_dir_stats(root: str = "/opt/axentx/surrogate-1") -> None:
    """Print a quick stat of the directory tree."""
    total_files = 0
    total_size = 0
    for p in Path(root).rglob("*"):
        if p.is_file():
            total_files += 1
            total_size += p.stat().st_size
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size / (1024**2):.2f} MiB")