#!/usr/bin/env python3
"""
Helm Values Token Validator

Validates Helm values files for unresolved template tokens ({{ .Values.* }}).
Supports merging a base values file with optional override values before validation.
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load and parse a YAML file."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in '{path}': {e}", file=sys.stderr)
        sys.exit(1)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge override dict into base dict.
    Override values take precedence over base values.
    """
    result = base.copy()
    for key, val in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(val, dict)
        ):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def find_unresolved_tokens(
    data: Any, 
    path: List[str] = None
) -> List[Tuple[List[str], str]]:
    """
    Recursively search for strings containing Helm template tokens.
    
    Returns:
        List of (path, token_string) tuples for unresolved tokens found.
    """
    if path is None:
        path = []

    unresolved = []

    if isinstance(data, dict):
        for key, val in data.items():
            unresolved.extend(find_unresolved_tokens(val, path + [key]))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            unresolved.extend(find_unresolved_tokens(item, path + [str(idx)]))
    elif isinstance(data, str):
        # Detect Helm template delimiters
        if "{{" in data and "}}" in data:
            unresolved.append((path, data))

    return unresolved


def format_report(unresolved: List[Tuple[List[str], str]]) -> str:
    """Generate human-readable report of unresolved tokens."""
    if not unresolved:
        return "All tokens resolved."
    
    lines = [f"ERROR: Found {len(unresolved)} unresolved token(s):"]
    for path, value in unresolved:
        lines.append(f"  - {'/'.join(path)}: {value}")
    return "\n".join(lines)


def validate_files(base_path: Path, override_path: Path | None = None) -> int:
    """
    Validate Helm values files for unresolved tokens.
    
    Returns:
        0 if all tokens resolved, 1 otherwise.
    """
    # Validate base file exists
    if not base_path.is_file():
        print(f"Error: Base values file '{base_path}' does not exist.", file=sys.stderr)
        return 1
    
    # Load base values
    base = load_yaml(base_path)
    
    # Load and merge override if provided
    if override_path:
        if not override_path.is_file():
            print(f"Error: Override values file '{override_path}' does not exist.", file=sys.stderr)
            return 1
        override = load_yaml(override_path)
        merged = deep_merge(base, override)
    else:
        merged = base
    
    # Detect unresolved tokens
    unresolved = find_unresolved_tokens(merged)
    
    # Output results
    print(format_report(unresolved))
    
    return 1 if unresolved else 0


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Helm values files for unresolved template tokens.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s values.yaml
  %(prog)s values.yaml --override custom-values.yaml
  %(prog)s values.yaml -v overrides.yaml
        """
    )
    parser.add_argument(
        "values",
        metavar="VALUES.yaml",
        type=Path,
        help="Path to the base Helm values file",
    )
    parser.add_argument(
        "--values", "-v",
        dest="override",
        type=Path,
        default=None,
        help="Optional override values file (deep-merged into base)",
    )
    
    args = parser.parse_args(argv)
    return validate_files(args.values, args.override)


if __name__ == "__main__":
    sys.exit(main())