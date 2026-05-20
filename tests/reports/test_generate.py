import unittest
import pandas as pd
from datetime import datetime
from src.reports.generate import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'date': [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)],
            'category': ['A', 'B', 'A'],
            'cost': [100, 200, 150]
        })
        self.report_generator = ReportGenerator(self.data)

    def test_generate_report(self):
        filtered_data = self.report_generator.generate_report('2023-01-01', '2023-01-03', ['A', 'B'])
        self.assertEqual(len(filtered_data), 3)

    def test_filter_data(self):
        filtered_data = self.report_generator._filter_data('2023-01-01', '2023-01-02', ['A'])
        self.assertEqual(len(filtered_data), 1)

    def test_export_to_csv(self):
        filtered_data = self.report_generator.generate_report('2023-01-01', '2023-01-03', ['A', 'B'])
        self.report_generator.export_to_csv(filtered_data, 'test_report.csv')
        self.assertTrue(os.path.exists('test_report.csv'))
        os.remove('test_report.csv')

    def test_export_to_pdf(self):
        filtered_data = self.report_generator.generate_report('2023-01-01', '2023-01-03', ['A', 'B'])
        self.report_generator.export_to_pdf(filtered_data, 'test_report.pdf')
        self.assertTrue(os.path.exists('test_report.pdf'))
        os.remove('test_report.pdf')

if __name__ == '__main__':
    unittest.main()