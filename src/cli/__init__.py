import argparse
import os
import subprocess
import sys
from axentx_surrogate_1.services.report_service import generate_investor_report

def main():
    parser = argparse.ArgumentParser(description="Generate investor report.")
    parser.add_argument("--format", choices=["pdf"], default="pdf", help="Report format")
    args = parser.parse_args()

    tenant_token = os.getenv("TENANT_TOKEN")
    if not tenant_token:
        print("Error: Tenant token is missing.")
        sys.exit(1)

    try:
        pdf_path = generate_investor_report(tenant_token, args.format)
        print(f"Investor report generated and saved to {pdf_path}")
        subprocess.Popen([pdf_path], shell=True)
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()