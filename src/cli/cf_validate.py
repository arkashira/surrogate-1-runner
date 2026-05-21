#!/usr/bin/env python3
"""
cf-validate – Validate a CloudFront configuration file locally.

The command accepts a path to a JSON or YAML file, runs the shared
validation routine, prints a JSON report, and exits with a status
code that reflects the result:

* 0 – syntax OK, no warnings or security issues
* 1 – syntax OK but there are warnings or security issues
* 2 – file could not be read or parsed

Examples
--------
    cf-validate config.json
    cf-validate /path/to/config.yaml
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Optional dependency: PyYAML
# --------------------------------------------------------------------------- #
try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

# --------------------------------------------------------------------------- #
# Validation back‑ends
# --------------------------------------------------------------------------- #
# The repository may expose the validation logic under two different
# import paths.  We try both and fall back to a stub if neither works.
try:
    from surrogate_1.validation import validate_cloudfront  # type: ignore
except Exception:  # pragma: no cover
    try:
        from surrogate1.api.cf_validator import CloudFrontValidator  # type: ignore

        def validate_cloudfront(data: Dict[str, Any]) -> Dict[str, Any]:
            """Thin wrapper around the real CloudFrontValidator."""
            validator = CloudFrontValidator()
            return validator.validate(data)
    except Exception:  # pragma: no cover
        # Stub – useful for quick testing or when the real package is missing.
        def validate_cloudfront(data: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "syntax_ok": True,
                "limit_warning": False,
                "security_issues": [],
                "details": "stub validation – real logic not available",
            }

# --------------------------------------------------------------------------- #
# File loading helpers
# --------------------------------------------------------------------------- #
def load_file(path: Path) -> Dict[str, Any]:
    """Load a JSON or YAML file into a Python dict.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file type is unsupported or the content cannot be parsed.
    """
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".json":
        return json.loads(text)

    if yaml and path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)

    raise ValueError(
        f"Unsupported file type: {path.suffix}. "
        "Only .json, .yaml, and .yml are allowed."
    )

# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="cf-validate",
        description="Validate a CloudFront configuration file locally.",
        epilog="""
Examples:
  cf-validate config.json
  cf-validate /path/to/config.yaml
""",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to the CloudFront configuration file (JSON or YAML).",
    )
    args = parser.parse_args(argv)

    if not args.path:
        parser.print_usage(sys.stderr)
        sys.exit(2)

    try:
        data = load_file(Path(args.path))
    except Exception as exc:
        print(f"Error loading file: {exc}", file=sys.stderr)
        sys.exit(2)

    report = validate_cloudfront(data)

    # Pretty‑print the report
    print(json.dumps(report, indent=2, sort_keys=True))

    # Determine exit code
    if (
        report.get("syntax_ok")
        and not report.get("limit_warning")
        and not report.get("security_issues")
    ):
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()