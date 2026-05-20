import unittest
from datetime import datetime, timedelta
from src.support.api import app

class SupportAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_submit_support_request(self):
        response = self.app.post('/support', json={'issue': 'Test issue'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['issue'], 'Test issue')
        self.assertEqual(data['status'], 'open')

    def test_get_support_request(self):
        response = self.app.post('/support', json={'issue': 'Test issue'})
        request_id = response.get_json()['id']
        response = self.app.get(f'/support/{request_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['issue'], 'Test issue')

    def test_update_support_request(self):
        response = self.app.post('/support', json={'issue': 'Test issue'})
        request_id = response.get_json()['id']
        response = self.app.put(f'/support/{request_id}', json={'status': 'closed'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'closed')

    def test_submit_feedback(self):
        response = self.app.post('/feedback', json={'feedback': 'Test feedback'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['feedback'], 'Test feedback')

if __name__ == '__main__':
    unittest.main()