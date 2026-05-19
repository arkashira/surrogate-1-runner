import unittest
from src.discrepancy_detection import DiscrepancyDetector

class TestDiscrepancyDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DiscrepancyDetector()
        self.invoice1 = {
            'id': '1',
            'amount': 100.0,
            'date': '2023-01-01',
            'vendor': 'Vendor A'
        }
        self.invoice2 = {
            'id': '2',
            'amount': 10000.0,
            'date': '2023-01-02',
            'vendor': 'Vendor B'
        }
        self.invoice3 = {
            'id': '3',
            'amount': 200.0,
            'date': '2023-01-03'
        }
        self.required_fields = ['id', 'amount', 'date', 'vendor']

    def test_detect_duplicates(self):
        self.assertFalse(self.detector.detect_duplicates(self.invoice1))
        self.assertTrue(self.detector.detect_duplicates(self.invoice1))

    def test_detect_unusual_amounts(self):
        self.assertFalse(self.detector.detect_unusual_amounts(self.invoice1, 1000.0))
        self.assertTrue(self.detector.detect_unusual_amounts(self.invoice2, 1000.0))

    def test_detect_missing_information(self):
        self.assertFalse(self.detector.detect_missing_information(self.invoice1, self.required_fields))
        self.assertTrue(self.detector.detect_missing_information(self.invoice3, self.required_fields))

    def test_detect_discrepancies(self):
        discrepancies = self.detector.detect_discrepancies(self.invoice1, 1000.0, self.required_fields)
        self.assertFalse(discrepancies['duplicate'])
        self.assertFalse(discrepancies['unusual_amount'])
        self.assertFalse(discrepancies['missing_information'])

        discrepancies = self.detector.detect_discrepancies(self.invoice2, 1000.0, self.required_fields)
        self.assertFalse(discrepancies['duplicate'])
        self.assertTrue(discrepancies['unusual_amount'])
        self.assertFalse(discrepancies['missing_information'])

        discrepancies = self.detector.detect_discrepancies(self.invoice3, 1000.0, self.required_fields)
        self.assertFalse(discrepancies['duplicate'])
        self.assertFalse(discrepancies['unusual_amount'])
        self.assertTrue(discrepancies['missing_information'])

if __name__ == '__main__':
    unittest.main()