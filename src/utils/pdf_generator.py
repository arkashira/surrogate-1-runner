
import os
from reportlab.pdfgen import canvas

def generate_pdf_from_buffer(pdf_buffer):
    with open("cost_report.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_buffer.read())

def generate_csv_from_data(data: List[dict]):
    fieldnames = ["Project", "Team", "Cost"]
    with open("cost_report.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)