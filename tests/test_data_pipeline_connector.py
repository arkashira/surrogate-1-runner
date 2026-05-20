import unittest
from src.data_pipeline_connector import DataPipelineConnector

class TestDataPipelineConnector(unittest.TestCase):
    def setUp(self):
        self.connector = DataPipelineConnector('Apache Beam', 'CSV')

    def test_connect_to_pipeline(self):
        self.assertIsNotNone(self.connector.connect_to_pipeline())

    def test_ingest_data(self):
        data = self.connector.ingest_data('tests/test_data.csv')
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()