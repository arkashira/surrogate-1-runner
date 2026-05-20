import unittest
from feedback_handler import app

class TestFeedbackHandler(unittest.TestCase):

    def test_collect_feedback(self):
        tester = app.test_client()
        data = {'name': 'John Doe', 'email': 'john@example.com', 'feedback': 'This is a test feedback'}
        response = tester.post('/feedback', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Feedback collected successfully')

if __name__ == '__main__':
    unittest.main()