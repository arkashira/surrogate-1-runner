import click
import os
import sys
from pathlib import Path
from typing import Optional

# Real imports for InvestorReportService and generate_pdf_report should be used in a real implementation
from investor_report_service import InvestorReportService, generate_pdf_report

def get_tenant_token() -> Optional[str]:
    """Get tenant token from environment variable."""
    return os.getenv('TENANT_TOKEN')

@click.command()
@click.option('--format', 'output_format', default='pdf', help='Output format (default: pdf)')
def report(output_format: str) -> None:
    """
    Generate and open the latest investor report.

    Currently only supports PDF format.
    """
    # Validate format
    if output_format not in ['pdf']:
        click.echo(f"Error: Unsupported format '{output_format}'. Only 'pdf' is supported.", err=True)
        sys.exit(1)

    # Check for tenant token
    tenant_token = get_tenant_token()
    if not tenant_token:
        click.echo("Error: TENANT_TOKEN environment variable is not set.", err=True)
        sys.exit(1)

    # Generate report
    output_file = 'investor_report.pdf'

    try:
        success = generate_pdf_report(output_file)
        if success:
            click.echo(f"Successfully generated {output_file}")
            click.echo(f"File path: {Path.cwd() / output_file}")
            open_pdf(output_file)
        else:
            click.echo("Error generating report.", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating report: {str(e)}", err=True)
        sys.exit(1)

def open_pdf(file_path: str) -> None:
    """Open the provided PDF file."""
    if os.name == 'posix':  # For Unix-like systems
        subprocess.run(['open', file_path], check=True)
    elif os.name == 'nt':  # For Windows
        subprocess.run(['start', file_path], check=True, shell=True)
    else:
        click.echo("Warning: Could not automatically open PDF")