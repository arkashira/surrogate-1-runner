import os
import json
import jinja2
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPORT_DIR = '/opt/axentx/surrogate-1/reports'

def load_compliance_data(account_id):
    """
    Loads compliance data from JSON file.

    Args:
        account_id (str): The ID of the account.

    Returns:
        dict: The loaded compliance data.
    """
    json_path = os.path.join(REPORT_DIR, f'{account_id}', 'compliance_report.json')
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {json_path}: {e}")
        sys.exit(1)

def generate_html_report(account_id, compliance_data):
    """
    Generates an HTML report using a Jinja2 template.

    Args:
        account_id (str): The ID of the account.
        compliance_data (dict): The compliance data.
    """
    # Load Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(REPORT_DIR),
        autoescape=True
    )

    # Get the template
    template_path = os.path.join(REPORT_DIR, f'{account_id}', 'compliance_template.html')
    try:
        template = env.get_template('compliance_template.html')
    except jinja2.TemplateNotFound as e:
        logger.error(f"Template not found: {e}")
        sys.exit(1)

    # Render the template
    try:
        html_output = template.render(
            account_id=account_id,
            summary=compliance_data.get('summary', {}),
            controls=compliance_data.get('controls', []),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        sys.exit(1)

    # Write output file
    output_path = os.path.join(REPORT_DIR, f'{account_id}', 'compliance.html')
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html_output)
        logger.info(f"Report generated successfully at {output_path}")
    except IOError as e:
        logger.error(f"Error writing report file: {e}")
        sys.exit(1)

def main(account_id):
    """
    Main function to generate and save the HTML report.

    Args:
        account_id (str): The ID of the account.
    """
    compliance_data = load_compliance_data(account_id)
    generate_html_report(account_id, compliance_data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python report_generator.py <account_id>")
        sys.exit(1)

    account_id = sys.argv[1]
    main(account_id)