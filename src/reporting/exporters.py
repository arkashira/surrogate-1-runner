
from typing import List
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styles["Heading1"].fontName = "Helvetica-Bold"
        self.styles["Heading2"].fontName = "Helvetica"
        self.styles["Heading2"].fontSize = 14
        self.styles["Heading3"].fontSize = 12

    def generate_pdf(self, data: List[dict]):
        doc = SimpleDocTemplate("cost_report.pdf", pagesize=letter)
        stories = []

        # Add title
        title = Paragraph("Investor-Ready Cost Report", self.styles["Heading1"])
        stories.append(title)

        # Add table with cost breakdowns
        table_headers = ["Project", "Team", "Cost"]
        table_data = [row for row in data]
        table = Table(table_headers + table_data, colWidths=([1.5*inch, 1.5*inch, 1.5*inch]))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.styles["Heading1"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.styles["Heading1"].fgColor),
            ('ALIGN', (0, 0), (-1, -1), TA_CENTER),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), self.styles["Heading2"]),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.styles["Heading2"].fgColor),
            ('GRID', (0, 0), (-1, -1), 1, self.styles["Heading2"])
        ]))
        stories.append(table)

        # Add chart showing cost trends
        # (This is a placeholder, as generating charts is a separate task)
        chart_image = Paragraph("Chart goes here", self.styles["Heading3"])
        stories.append(chart_image)

        # Add footer
        footer = Paragraph("Generated at {date}", self.styles["Heading3"])
        footer.date = doc.now()
        stories.append(footer)

        doc.build(stories)

        # Return the PDF as a BytesIO object
        pdf_buffer = BytesIO()
        doc.save(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer