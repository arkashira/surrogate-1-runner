#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from surrogate_1.engine import scan_solidity_files

def main():
    parser = argparse.ArgumentParser(description='Scan Solidity files for findings.')
    parser.add_argument('path', type=str, help='Path to Solidity files or directory')
    parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path '{path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    findings = scan_solidity_files(path)

    if args.format == 'json':
        print(json.dumps(findings, indent=2))
    else:
        print_findings_table(findings)

    if any(finding['severity'] == 'HIGH' for finding in findings):
        sys.exit(1)

def print_findings_table(findings: List[Dict[str, Any]]):
    if not findings:
        print("No findings.")
        return

    print("{:<50} {:<10} {:<20} {:<10}".format("File", "Line", "Finding", "Severity"))
    print("-" * 100)
    for finding in findings:
        print("{:<50} {:<10} {:<20} {:<10}".format(
            finding['file'],
            finding['line'],
            finding['finding'],
            finding['severity']
        ))

if __name__ == '__main__':
    main()