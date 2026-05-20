import unittest
from scripts.ingest_components import ingest_data

class TestIngestComponents(unittest.TestCase):
    def test_ingest_data(self):
        # Test the ingest_data function
        ingest_data()

if __name__ == '__main__':
    unittest.main()