import argparse
import os
from pathlib import Path

def scan_contracts(path):
    findings = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.sol'):
                file_path = Path(root) / file
                with open(file_path, 'r') as f:
                    for line_number, line in enumerate(f, 1):
                        # Check for Solidity version pragma
                        if 'pragma solidity' in line:
                            findings.append({
                                'severity': 'info',
                                'file': str(file_path),
                                'line': line_number,
                                'description': 'Solidity version pragma found'
                            })
                        # Check for public functions (potential security risk)
                        if 'function' in line and 'public' in line:
                            findings.append({
                                'severity': 'warning',
                                'file': str(file_path),
                                'line': line_number,
                                'description': 'Public function found'
                            })
    return findings

def main():
    parser = argparse.ArgumentParser(description='Security scanner for Solidity contracts')
    subparsers = parser.add_subparsers(dest='command', required=True)

    scan_parser = subparsers.add_parser('scan', help='Scan a directory for security issues')
    scan_parser.add_argument('path', help='Path to the directory containing Solidity contracts')

    args = parser.parse_args()

    if args.command == 'scan':
        findings = scan_contracts(args.path)
        if findings:
            print("Security findings:")
            for finding in findings:
                print(f"Severity: {finding['severity']}")
                print(f"File: {finding['file']}")
                print(f"Line: {finding['line']}")
                print(f"Description: {finding['description']}")
                print()
            sys.exit(1)
        else:
            print("No security findings detected.")
            sys.exit(0)

if __name__ == '__main__':
    main()