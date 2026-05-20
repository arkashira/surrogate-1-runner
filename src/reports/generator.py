import csv
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, data):
        self.data = data

    def generate_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Department', 'Project', 'Cost']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

    def generate_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Cost Breakdown Report", ln=True, align='C')
        pdf.cell(200, 10, txt="", ln=True)
        pdf.cell(200, 10, txt="Department | Project | Cost", ln=True, align='L')
        for row in self.data:
            pdf.cell(200, 10, txt=f"{row['Department']} | {row['Project']} | {row['Cost']}", ln=True, align='L')
        pdf.output(filename)

def main():
    sample_data = [
        {'Department': 'Sales', 'Project': 'ProjectA', 'Cost': 1000},
        {'Department': 'Marketing', 'Project': 'ProjectB', 'Cost': 1500},
        # Add more sample data as needed
    ]
    generator = ReportGenerator(sample_data)
    generator.generate_csv('cost_breakdown.csv')
    generator.generate_pdf('cost_breakdown.pdf')

if __name__ == "__main__":
    main()