import pytest
import csv
import os
from ingest.csv_parser import parse_csv

@pytest.fixture
def sample_csv():
    # Create a sample CSV file with 100 rows for testing
    csv_path = "sample.csv"
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "name", "value"])
        for i in range(100):
            writer.writerow([i, f"name_{i}", i * 10])
    yield csv_path
    # Clean up the sample CSV file after the test
    os.remove(csv_path)

def test_parse_csv(sample_csv):
    # Test parsing of the sample CSV file
    data = parse_csv(sample_csv)
    assert len(data) == 100
    assert data[0] == {"id": 0, "name": "name_0", "value": 0}
    assert data[99] == {"id": 99, "name": "name_99", "value": 990}

def test_parse_csv_empty_file():
    # Test parsing of an empty CSV file
    csv_path = "empty.csv"
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "name", "value"])
    data = parse_csv(csv_path)
    assert len(data) == 0
    os.remove(csv_path)