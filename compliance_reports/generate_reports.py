import os
import json
import sys
from .checker import ComplianceChecker

def main(artifacts_dir, output_dir):
    """
    Scan all files under artifacts_dir, run compliance checks,
    and write a JSON report to output_dir.
    """
    checker = ComplianceChecker()
    reports = {}

    for root, _, files in os.walk(artifacts_dir):
        for file in files:
            path = os.path.join(root, file)
            violations = checker.check_artifact(path)
            reports[file] = {
                "path": path,
                "violations": violations,
                "compliant": len(violations) == 0,
            }

    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "compliance_report.json")
    with open(report_path, "w") as f:
        json.dump(reports, f, indent=2)

    print(f"Compliance report written to {report_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_reports.py <artifacts_dir> <output_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])