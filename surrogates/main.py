import argparse
import json
import sys
from typing import List, Dict

from surrogates.analysis import LintContext, LintResult, get_rules
from surrogates.config import load_config

def main():
    parser = argparse.ArgumentParser(description="Surrogate code analysis tool")
    parser.add_argument("files", nargs="*", help="Files to analyze")
    args = parser.parse_args()

    config = load_config()
    context = LintContext()
    rules = get_rules(config)

    results: List[LintResult] = []

    for file_path in args.files:
        try:
            with open(file_path, "r") as f:
                source = f.read()
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}", file=sys.stderr)
            continue

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
            continue

        for rule in rules:
            rule.visit(tree, context)
            results.extend(rule.results)

    if results:
        for result in results:
            print(f"Severity: {result.severity.value} - {result.message}")
            print(f"File: {result.file_path}, Line: {result.line}")
            print(f"Details: {result.details}")
            print("-" * 60)
    else:
        print("No issues found.")

if __name__ == "__main__":
    main()