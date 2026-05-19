"""
Coverage Formatter Module

This module provides utilities to format and display test coverage
information for the surrogate test runner. It is used by the
`surrogate test-filter` CLI command to present coverage percentages
for each filtered test.

The module expects coverage data in the form of a dictionary mapping
test names to coverage percentages (float values between 0 and 100).
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple
import re
import sys


def filter_tests_by_tags(
    tests: Iterable[str], tags: List[str]
) -> List[str]:
    """
    Return a list of test names that contain any of the specified tags.

    Parameters
    ----------
    tests : Iterable[str]
        Iterable of test names.
    tags : List[str]
        List of tag strings to filter by.

    Returns
    -------
    List[str]
        Filtered list of test names.
    """
    if not tags:
        return list(tests)

    tag_patterns = [re.compile(tag) for tag in tags]
    filtered = []
    for test in tests:
        if any(p.search(test) for p in tag_patterns):
            filtered.append(test)
    return filtered


def format_coverage(
    coverage_map: Dict[str, float], tests: Iterable[str]
) -> str:
    """
    Format coverage information for a list of tests.

    Parameters
    ----------
    coverage_map : Dict[str, float]
        Mapping from test name to coverage percentage.
    tests : Iterable[str]
        Iterable of test names to format.

    Returns
    -------
    str
        Formatted string with one line per test:
        "<test_name> : <coverage>%"
    """
    lines = []
    for test in tests:
        percent = coverage_map.get(test, 0.0)
        lines.append(f"{test} : {percent:.2f}%")
    return "\n".join(lines)


def load_coverage_report(report_path: str) -> Dict[str, float]:
    """
    Load a coverage report from a simple CSV file.

    The CSV is expected to have two columns: test_name,coverage_percent
    with a header row.

    Parameters
    ----------
    report_path : str
        Path to the coverage CSV report.

    Returns
    -------
    Dict[str, float]
        Mapping from test name to coverage percentage.
    """
    coverage = {}
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            header = f.readline()
            for line in f:
                parts = line.strip().split(",")
                if len(parts) != 2:
                    continue
                test_name, percent_str = parts
                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0.0
                coverage[test_name] = percent
    except FileNotFoundError:
        pass
    return coverage


def main(argv: List[str] | None = None) -> None:
    """
    CLI entry point for `surrogate test-filter`.

    Usage:
        surrogate test-filter --tags=smoke,regression --coverage=coverage.csv
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Filter tests by tags and display coverage."
    )
    parser.add_argument(
        "--tags",
        type=str,
        default="",
        help="Comma-separated list of tags or regex patterns to filter tests.",
    )
    parser.add_argument(
        "--coverage",
        type=str,
        default="",
        help="Path to a CSV coverage report file.",
    )
    parser.add_argument(
        "tests",
        nargs="*",
        help="Optional list of test names to filter. If omitted, all tests are considered.",
    )
    args = parser.parse_args(argv)

    # Load all available tests from the provided list or a default source.
    # For this example, we assume tests are passed via CLI; otherwise,
    # a real implementation would discover tests from the test suite.
    all_tests = args.tests if args.tests else []

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    filtered = filter_tests_by_tags(all_tests, tags)

    coverage_map = {}
    if args.coverage:
        coverage_map = load_coverage_report(args.coverage)

    output = format_coverage(coverage_map, filtered)
    print(output)


if __name__ == "__main__":
    main(sys.argv[1:])