import json
from jinja2 import Environment, FileSystemLoader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import HTML

def generate_compliance_report(compliance_data, output_pdf_path, output_json_path):
    """
    Generates a PDF and JSON compliance report based on the provided compliance data.

    Args:
        compliance_data (dict): Dictionary containing compliance check results.
                               Expected keys: 'encryption_at_rest', 'access_logging', 'network_isolation'.
                               Values should be boolean or a string indicating status.
        output_pdf_path (str): Path to save the generated PDF.
        output_json_path (str): Path to save the generated JSON.
    """
    # Load the HTML template
    env = Environment(loader=FileSystemLoader('/opt/axentx/surrogate-1/templates'))
    template = env.get_template('report-template.html')
    rendered_html = template.render(compliance_data)

    # Generate PDF report
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    html_width, html_height = 612, 792  # A4 in points (converted to letter size)
    c.setFont("Helvetica", 12)
    html = HTML(rendered_html)
    html.wrapOn(c, html_width, html_height)
    html.drawOn(c, 50, 750)  # Position the HTML content on the page
    c.save()

    # Generate JSON report
    with open(output_json_path, 'w') as json_file:
        json.dump(compliance_data, json_file, indent=2)

if __name__ == "__main__":
    # Example usage
    compliance_example = {
        "encryption_at_rest": True,
        "access_logging": True,
        "network_isolation": True
    }
    generate_compliance_report(compliance_example, "compliance_report.pdf", "compliance_report.json")