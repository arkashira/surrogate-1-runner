
import os
from weasyprint import HTML
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def generate_pdf(tenant_id, data):
    if not data:
        data = {"note": "Required data is missing."}

    # Create a simple HTML string with the data
    html_string = f"""
    <html>
    <head></head>
    <body>
    <h1>Cloud Spend Report</h1>
    <p>Total Spend: ${data['total_spend']:.2f}</p>
    <p>% Change vs. Prior Month: {data['percent_change']:.2f}%</p>
    <h2>Top 3 Cost Drivers</h2>
    <ul>
    {'<li>'.join([f'{cost[0]}: ${cost[1]:.2f}' for cost in data['top_costs']])}
    </ul>
    <h2>Top 3 Savings Recommendations</h2>
    <ul>
    {'<li>'.join([f'{recommendation}' for recommendation in data['savings_recommendations']])}
    </ul>
    <p>{data.get('note', '')}</p>
    </body>
    </html>
    """

    # Convert HTML to PDF using WeasyPrint
    html = HTML(string=html_string)
    pdf_file = f"/opt/axentx/surrogate-1/reports/{tenant_id}/latest.pdf"
    html.write_pdf(pdf_file)

    # Ensure the PDF size is less than or equal to 500KB
    if os.path.getsize(pdf_file) > 500 * 1024:
        os.remove(pdf_file)
        raise Exception("Generated PDF size exceeds 500KB.")

# Example usage:
# generate_pdf("test_tenant", {"total_spend": 12345.67, "percent_change": 2.5, "top_costs": [("AWS", 5000), ("GCP", 3000), ("Azure", 2000)], "savings_recommendations": ["Optimize usage", "Negotiate better pricing", "Use spot instances"]})