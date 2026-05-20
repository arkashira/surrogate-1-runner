import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='AxentX CLI')
    parser.add_argument('--fail-on-severity', choices=['LOW', 'MEDIUM', 'HIGH'], default='HIGH', help='Treat findings of this severity as failures')
    return parser.parse_args()

def main():
    args = parse_args()

    # Assume we have a function `get_findings()` that returns a list of findings
    findings = get_findings()

    if any(f.severity == args.fail_on_severity for f in findings):
        print(f"Found {len(findings)} {args.fail_on_severity.upper()} findings. Exiting with code 1.")
        sys.exit(1)

if __name__ == "__main__":
    main()