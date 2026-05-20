import unittest
from unittest.mock import patch, MagicMock
from your_application import verify_badge  # Import the function to test
import json

class TestVerificationLogic(unittest.TestCase):

    @patch('your_application.secret_key', 'your_secret_key_here')
    def test_verify_badge_valid(self):
        # Mock a valid badge
        badge_id = "valid_badge_id"
        mock_badge = {
            "badge_id": badge_id,
            "signature": "valid_signature"
        }
        mock_request = MagicMock()
        mock_request.args.get.return_value = badge_id

        # Mock the verification function to return a valid response
        with patch('your_application.verify_signature', return_value=True):
            response = verify_badge(mock_request)

            self.assertEqual(response.status_code, 200)
            self.assertIn('valid', response.json['status'])

    @patch('your_application.secret_key', 'your_secret_key_here')
    def test_verify_badge_invalid(self):
        # Mock an invalid badge
        badge_id = "invalid_badge_id"
        mock_badge = {
            "badge_id": badge_id,
            "signature": "invalid_signature"
        }
        mock_request = MagicMock()
        mock_request.args.get.return_value = badge_id

        # Mock the verification function to return an invalid response
        with patch('your_application.verify_signature', return_value=False):
            response = verify_badge(mock_request)

            self.assertEqual(response.status_code, 400)
            self.assertIn('invalid', response.json['status'])

    @patch('your_application.secret_key', 'your_secret_key_here')
    def test_verify_badge_tampered(self):
        # Mock a tampered badge
        badge_id = "tampered_badge_id"
        mock_badge = {
            "badge_id": badge_id,
            "signature": "tampered_signature"
        }
        mock_request = MagicMock()
        mock_request.args.get.return_value = badge_id

        # Mock the verification function to raise an exception for tampered badge
        with patch('your_application.verify_signature', side_effect=Exception('Tampered badge')):
            response = verify_badge(mock_request)

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_response_time(self):
        # Test that the response time is less than 200ms for 95% of calls
        import time
        badge_id = "valid_badge_id"
        mock_request = MagicMock()
        mock_request.args.get.return_value = badge_id

        response_times = []
        for _ in range(100):
            start_time = time.time()
            verify_badge(mock_request)
            end_time = time.time()
            response_times.append(end_time - start_time)

        response_times.sort()
        percentile_95_time = response_times[int(0.95 * len(response_times))]
        self.assertLess(percentile_95_time, 0.2)

if __name__ == '__main__':
    unittest.main()