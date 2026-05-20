import unittest
from web.app.controllers.feedback_controller import app, store_feedback

class TestFeedbackController(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_submit_feedback(self):
        response = self.app.post('/submit_feedback', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'feedback': 'This is a test feedback.'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for your feedback!', response.data)

    def test_store_feedback(self):
        store_feedback('Test User', 'test@example.com', 'This is a test feedback.')
        # Add assertions based on how feedback is stored (e.g., check database)

if __name__ == '__main__':
    unittest.main()