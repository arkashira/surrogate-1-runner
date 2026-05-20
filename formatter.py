"""
Utility used by the pre‑commit hook to verify that staged Python files are
formatted with Black.

The module can also be executed directly (`python -m formatter`) to run the
check on the whole repository – useful for CI pipelines.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def _run_black_check(file_path: Path) -> Tuple[bool, str]:
    """
    Run ``black --quiet --check`` on *file_path*.

    Returns
    -------
    (is_formatted, output)
        *is_formatted* – ``True`` if Black exits with ``0`` (already formatted).
        *output* – combined stdout/stderr for reporting.
    """
    try:
        result = subprocess.run(
            ["black", "--quiet", "--check", str(file_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        # 0 → already formatted, 1 → would reformat, >1 → error
        return result.returncode == 0, result.stdout + result.stderr
    except FileNotFoundError:
        # Black not installed – give a deterministic, user‑friendly message.
        msg = (
            "ERROR: Black formatter not found.\n"
            "Install it with:  pip install black\n"
        )
        return False, msg
    except Exception as exc:  # pragma: no cover – defensive programming
        return False, f"Unexpected error while running Black: {exc}\n"


def check_formatting(file_paths: List[Path]) -> List[str]:
    """
    Validate a collection of files.

    Parameters
    ----------
    file_paths : List[Path]
        Absolute ``Path`` objects pointing at the files to check.

    Returns
    -------
    List[str]
        Human‑readable issue strings. Empty when everything is fine.
    """
    issues: List[str] = []
    for path in file_paths:
        if not path.is_file():
            # Skip deleted/renamed files that may still appear in the diff.
            continue
        ok, out = _run_black_check(path)
        if not ok:
            issues.append(f"Formatting issue in {path}:\n{out.strip()}")
    return issues


def _staged_python_files(repo_root: Path) -> List[Path]:
    """
    Query *git* for staged ``.py`` files and return them as absolute ``Path`` objects.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        # If git fails we treat it as a fatal error – the hook should not silently pass.
        sys.stderr.write(f"git error while gathering staged files: {exc}\n")
        sys.exit(2)

    files = [
        repo_root / p
        for p in result.stdout.splitlines()
        if p.strip().endswith(".py")
    ]
    return files


def main() -> int:
    """
    Entry‑point used by the Bash wrapper and by ``python -m formatter``.
    Returns an exit‑code suitable for a pre‑commit hook:
        0 – all good
        1 – formatting problems
        2 – internal error (e.g. git failure)
    """
    repo_root = Path(__file__).resolve().parent  # /opt/axentx/surrogate-1
    files = _staged_python_files(repo_root)

    if not files:
        # Nothing to check – succeed silently.
        return 0

    issues = check_formatting(files)
    if issues:
        sys.stdout.write("\n".join(issues) + "\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())