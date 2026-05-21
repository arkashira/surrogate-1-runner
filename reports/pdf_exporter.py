import os
from fpdf import FPDF

class PDFExporter:
    def __init__(self, report_data):
        self.report_data = report_data

    def create_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.cell(200, 10, txt="Audit Evidence Report", ln=True, align='C')

        # Add report data
        for key, value in self.report_data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        # Save the PDF
        pdf.output(filename)

def generate_audit_report(report_data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = os.path.join(output_dir, 'audit_evidence_report.pdf')
    exporter = PDFExporter(report_data)
    exporter.create_pdf(filename)
    return filename

# Example usage
if __name__ == "__main__":
    sample_report_data = {
        "Report ID": "RPT-2023-001",
        "Date": "2023-10-01",
        "Description": "This is a sample audit evidence report."
    }
    output_directory = "/tmp/audit_reports"
    report_filename = generate_audit_report(sample_report_data, output_directory)
    print(f"Audit report generated at: {report_filename}")