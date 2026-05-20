import json
import csv
import os
import pdfkit
from datetime import datetime
from typing import List, Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from jinja2 import Template

class InconsistencyReport:
    def __init__(self, inconsistencies: List[Dict[str, Any]]):
        """
        Initialize the report generator with a list of detected inconsistencies.
        Each inconsistency should have:
        - id: str (unique identifier)
        - type: str (type of inconsistency)
        - severity: str (e.g., 'low', 'medium', 'high')
        - description: str (detailed description)
        - suggested_fix: str (recommended fix)
        - workaround: str (alternative solution)
        """
        self.inconsistencies = inconsistencies
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.report_data = self._process_inconsistencies()

    def _process_inconsistencies(self) -> List[Dict[str, Any]]:
        processed_data = []
        for inconsistency in self.inconsistencies:
            processed_data.append({
                "id": inconsistency.get("id", ""),
                "type": inconsistency.get("type", ""),
                "severity": inconsistency.get("severity", ""),
                "description": inconsistency.get("description", ""),
                "suggested_fix": inconsistency.get("suggested_fix", "No suggested fix available"),
                "workaround": inconsistency.get("workaround", "No workaround available"),
                "timestamp": self.timestamp
            })
        return processed_data

    def generate_html(self, output_path: str) -> None:
        """Generate an HTML report with styling and structure."""
        html_template = Template("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Inconsistency Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #b00020; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Inconsistency Report</h1>
            <p>Generated on: {{ timestamp }}</p>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Description</th>
                    <th>Suggested Fix</th>
                    <th>Workaround</th>
                </tr>
                {% for item in inconsistencies %}
                <tr>
                    <td>{{ item.id }}</td>
                    <td>{{ item.type }}</td>
                    <td>{{ item.severity }}</td>
                    <td>{{ item.description }}</td>
                    <td>{{ item.suggested_fix }}</td>
                    <td>{{ item.workaround }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """)
        with open(output_path, 'w') as f:
            f.write(html_template.render(inconsistencies=self.report_data, timestamp=self.timestamp))

    def generate_pdf(self, output_path: str) -> None:
        """Generate a PDF report using ReportLab."""
        pdf = canvas.Canvas(output_path, pagesize=A4)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(50, 750, f"Inconsistency Report - Generated on: {self.timestamp}")
        pdf.setFont("Helvetica", 12)

        y = 700
        for inconsistency in self.report_data:
            pdf.drawString(50, y, f"ID: {inconsistency['id']}")
            pdf.drawString(50, y - 30, f"Type: {inconsistency['type']}")
            pdf.drawString(50, y - 60, f"Severity: {inconsistency['severity']}")
            pdf.drawString(50, y - 90, f"Description: {inconsistency['description']}")
            pdf.drawString(50, y - 120, f"Suggested Fix: {inconsistency['suggested_fix']}")
            pdf.drawString(50, y - 150, f"Workaround: {inconsistency['workaround']}")
            y -= 180

        pdf.save()

    def generate_csv(self, output_path: str) -> None:
        """Generate a CSV report."""
        keys = self.report_data[0].keys() if self.report_data else []
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.report_data)

# Example usage
if __name__ == "__main__":
    inconsistencies = [
        {
            "id": "001",
            "type": "Data Type Mismatch",
            "severity": "High",
            "description": "Expected integer but found string",
            "suggested_fix": "Convert string to integer",
            "workaround": "Use string operations instead"
        },
        {
            "id": "002",
            "type": "Missing Field",
            "severity": "Medium",
            "description": "Field 'email' is missing",
            "suggested_fix": "Add the missing field",
            "workaround": "Use default value"
        }
    ]
    report_generator = InconsistencyReport(inconsistencies)
    report_generator.generate_html("inconsistency_report.html")
    report_generator.generate_pdf("inconsistency_report.pdf")
    report_generator.generate_csv("inconsistency_report.csv")