
import os
import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_incident_report(data: Dict[str, Any], preferences: Dict[str, Any]) -> str:
    style_sheet = getSampleStyleSheet()
    doc = SimpleDocTemplate(f"incident_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", pagesize=letter)

    elements = []
    elements.append(Paragraph(f"Incident Report", style_sheet['Title']))
    elements.append(Spacer(1, 12))

    for key, value in data.items():
        elements.append(Paragraph(f"{key}: {value}", style_sheet['Heading1']))
        elements.append(Spacer(1, 6))

    elements.append(Paragraph("Additional details:", style_sheet['Heading2']))
    elements.append(Spacer(1, 6))

    for key, value in preferences.items():
        elements.append(Paragraph(f"{key}: {value}", style_sheet['BodyText']))
        elements.append(Spacer(1, 6))

    doc.build(elements)

    with open(f"incident_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", "rb") as file:
        report = file.read()

    os.remove("incident_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    return report