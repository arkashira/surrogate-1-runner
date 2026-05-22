import argparse
import os
import sys
import pathlib
from typing import List

# Mapping of language identifiers to file extensions that can be formatted.
SUPPORTED_EXT = {
    "python": [".py"],
    "javascript": [".js", ".jsx"],
    "typescript": [".ts", ".tsx"],
    "go": [".go"],
    # Extend as needed.
}
# Flattened list of all supported extensions (used when no language is supplied).
ALL_EXT = [ext for exts in SUPPORTED_EXT.values() for ext in exts]


def _format_file(path: pathlib.Path) -> bool:
    """
    Placeholder formatter: reads the file and writes the same content back.
    Returns True on success, False on any exception.
    """
    try:
        data = path.read_bytes()
        path.write_bytes(data)
        return True
    except Exception:
        return False


def _gather_target_files(repo: pathlib.Path, extensions: List[str]) -> List[pathlib.Path]:
    """
    Walk the repository and collect files whose suffix matches one of the supplied extensions.
    """
    targets = []
    for root, _, files in os.walk(repo):
        for fname in files:
            if pathlib.Path(fname).suffix in extensions:
                targets.append(pathlib.Path(root) / fname)
    return targets


def run(args: argparse.Namespace) -> int:
    """
    Core implementation of the `surrogate format` command.
    Returns an exit code (0 on success, 1 on failure).
    """
    repo_path = pathlib.Path(args.repo).resolve()
    if not repo_path.is_dir():
        print(f"Error: repository path '{repo_path}' does not exist or is not a directory.", file=sys.stderr)
        return 1

    # Determine which extensions to process.
    if args.lang:
        extensions = SUPPORTED_EXT.get(args.lang.lower())
        if not extensions:
            print(f"Error: unsupported language '{args.lang}'.", file=sys.stderr)
            return 1
    else:
        extensions = ALL_EXT

    target_files = _gather_target_files(repo_path, extensions)

    formatted = 0
    failed = 0
    for file_path in target_files:
        if _format_file(file_path):
            formatted += 1
        else:
            failed += 1

    print(f"Formatted {formatted} file(s).")
    if failed:
        print(f"Failed to format {failed} file(s).", file=sys.stderr)
        return 1

    return 0


def build_parser(parent_parser: argparse.ArgumentParser) -> None:
    """
    Attach the `format` sub‑command to an existing argparse parser.
    """
    parser = parent_parser.add_parser(
        "format",
        help="Format all supported source files in a repository.",
        description="Formats code files in the given repository and prints a summary.",
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Path to the repository to format.",
    )
    parser.add_argument(
        "--lang",
        help="Optional language filter (e.g., python, javascript).",
    )
    parser.set_defaults(_func=run)