import os
import csv
from unittest.mock import patch
from src.reports.generator import ReportGenerator

def test_generate_csv():
    sample_data = [
        {'Department': 'Sales', 'Project': 'ProjectA', 'Cost': 1000},
        {'Department': 'Marketing', 'Project': 'ProjectB', 'Cost': 1500},
    ]
    generator = ReportGenerator(sample_data)
    generator.generate_csv('test_cost_breakdown.csv')
    
    with open('test_cost_breakdown.csv', mode='r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
        
    assert len(rows) == 2
    assert rows[0]['Department'] == 'Sales'
    assert rows[0]['Project'] == 'ProjectA'
    assert int(rows[0]['Cost']) == 1000
    
    os.remove('test_cost_breakdown.csv')

@patch('FPDF.output')
def test_generate_pdf(mock_output):
    sample_data = [
        {'Department': 'Sales', 'Project': 'ProjectA', 'Cost': 1000},
        {'Department': 'Marketing', 'Project': 'ProjectB', 'Cost': 1500},
    ]
    generator = ReportGenerator(sample_data)
    generator.generate_pdf('test_cost_breakdown.pdf')
    
    mock_output.assert_called_once_with('test_cost_breakdown.pdf')