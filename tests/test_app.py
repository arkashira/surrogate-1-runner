import unittest
from app import app

class TestComplianceStatus(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_compliance_status(self):
        response = self.app.get('/compliance-status')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'status', response.data)

if __name__ == '__main__':
    unittest.main()