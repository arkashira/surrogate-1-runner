import unittest
from src.utils.data_sanitizer import sanitize_data

class TestDataSanitizer(unittest.TestCase):
    def test_sanitize_data(self):
        test_data = {
            'name': 'John Doe',
            'ssn': '123-45-6789',
            'credit_card': '1234567890123456',
            'address': {
                'street': '123 Main St',
                'city': 'Anytown',
                'zip': '12345'
            }
        }
        sanitized_data = sanitize_data(test_data)
        self.assertEqual(sanitized_data['ssn'], '[REDACTED SSN]')
        self.assertEqual(sanitized_data['credit_card'], '[REDACTED CREDIT CARD]')
        self.assertEqual(sanitized_data['address']['street'], '123 Main St')

if __name__ == '__main__':
    unittest.main()