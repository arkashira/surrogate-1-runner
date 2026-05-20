import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os

class ReportGenerator:
    def __init__(self, data):
        self.data = data

    def generate_report(self, start_date, end_date, categories):
        filtered_data = self._filter_data(start_date, end_date, categories)
        return filtered_data

    def _filter_data(self, start_date, end_date, categories):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_data = self.data[
            (self.data['date'] >= start_date) &
            (self.data['date'] <= end_date) &
            (self.data['category'].isin(categories))
        ]
        return filtered_data

    def export_to_csv(self, data, file_path):
        data.to_csv(file_path, index=False)

    def export_to_pdf(self, data, file_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for index, row in data.iterrows():
            pdf.cell(200, 10, txt=str(row), ln=True, align='L')

        pdf.output(file_path)

# Example usage
if __name__ == "__main__":
    data = pd.DataFrame({
        'date': [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)],
        'category': ['A', 'B', 'A'],
        'cost': [100, 200, 150]
    })

    report_generator = ReportGenerator(data)
    filtered_data = report_generator.generate_report('2023-01-01', '2023-01-03', ['A', 'B'])

    report_generator.export_to_csv(filtered_data, 'report.csv')
    report_generator.export_to_pdf(filtered_data, 'report.pdf')