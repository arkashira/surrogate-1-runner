"""
Coverage report generator for surrogate-1.

This module loads the coverage data produced by `coverage run` (default
`.coverage` file), computes overall coverage, per-file uncovered lines,
and generates two artifacts:
  * coverage_report.json
  * coverage_report.md

The JSON output is machine‑readable and can be consumed by CI
pipelines. The Markdown output is human‑friendly and suitable for
embedding in release notes or PR comments.

The module can be executed as a script:

    python -m report_generator [--coverage-file <path>] [--output-dir <dir>]

If no coverage file is provided, the default `.coverage` in the current
working directory is used. If no output directory is provided, the
current working directory is used.

Author: axentx
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    # coverage is a heavy dependency; import lazily to avoid import errors
    from coverage import CoverageData
except Exception as exc:  # pragma: no cover
    # Provide a clear error message if coverage is missing
    raise RuntimeError(
        "The `coverage` package is required to generate reports. "
        "Install it with `pip install coverage`."
    ) from exc


def load_coverage_data(coverage_file: Path) -> CoverageData:
    """Load coverage data from the given file."""
    data = CoverageData()
    data.read_file(str(coverage_file))
    return data


def compute_overall_coverage(data: CoverageData) -> float:
    """Return overall coverage percentage (0-100)."""
    total_statements = 0
    total_executed = 0
    for file_stat in data.measured_files():
        totals = data.file_data(file_stat)
        total_statements += totals["statements"]
        total_executed += totals["executed"]
    if total_statements == 0:
        return 100.0
    return round((total_executed / total_statements) * 100, 2)


def uncovered_lines_per_file(data: CoverageData) -> Dict[str, List[int]]:
    """Return a mapping from file path to list of uncovered line numbers."""
    result: Dict[str, List[int]] = {}
    for file_path in data.measured_files():
        uncovered = data.lines(file_path, missing=True)
        if uncovered:
            result[file_path] = sorted(uncovered)
    return result


def recommend_tests(uncovered: List[int]) -> str:
    """
    Very naive recommendation: if there are uncovered lines, suggest
    writing tests for those lines. In a real system this could be
    replaced with a smarter heuristic or integration with a test
    generator.
    """
    if not uncovered:
        return "All lines covered."
    return f"Consider adding tests for lines: {', '.join(map(str, uncovered))}"


def generate_json_report(
    overall: float,
    uncovered_map: Dict[str, List[int]],
    output_path: Path,
) -> None:
    """Write the JSON report to the given path."""
    report = {
        "overall_coverage_percent": overall,
        "files": [
            {
                "path": file_path,
                "uncovered_lines": lines,
                "recommended_tests": recommend_tests(lines),
            }
            for file_path, lines in uncovered_map.items()
        ],
    }
    output_path.write_text(json.dumps(report, indent=2))
    print(f"JSON report written to {output_path}")


def generate_markdown_report(
    overall: float,
    uncovered_map: Dict[str, List[int]],
    output_path: Path,
) -> None:
    """Write the Markdown report to the given path."""
    lines = [
        "# Coverage Report",
        "",
        f"**Overall Coverage:** {overall:.2f}%",
        "",
        "## Uncovered Lines by File",
        "",
        "| File | Uncovered Lines | Recommendation |",
        "|------|-----------------|----------------|",
    ]

    for file_path, lines_uncovered in sorted(uncovered_map.items()):
        rec = recommend_tests(lines_uncovered)
        lines.append(
            f"| `{file_path}` | {', '.join(map(str, lines_uncovered))} | {rec} |"
        )

    output_path.write_text("\n".join(lines))
    print(f"Markdown report written to {output_path}")


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate coverage reports in JSON and Markdown."
    )
    parser.add_argument(
        "--coverage-file",
        type=Path,
        default=Path(".coverage"),
        help="Path to the coverage data file (default: .coverage)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory to write the reports (default: current directory)",
    )
    args = parser.parse_args(argv)

    if not args.coverage_file.exists():
        print(f"Coverage file not found: {args.coverage_file}", file=sys.stderr)
        sys.exit(1)

    data = load_coverage_data(args.coverage_file)
    overall = compute_overall_coverage(data)
    uncovered_map = uncovered_lines_per_file(data)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "coverage_report.json"
    md_path = output_dir / "coverage_report.md"

    generate_json_report(overall, uncovered_map, json_path)
    generate_markdown_report(overall, uncovered_map, md_path)


if __name__ == "__main__":  # pragma: no cover
    main()