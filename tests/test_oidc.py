import unittest
from services.auth.oidc import app, oauth

class TestOIDC(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_redirect(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response.headers)
        self.assertTrue(response.headers['Location'].startswith('https://your-okta-domain/oauth2/default/v1/authorize'))

    def test_authorize(self):
        # Mock the authorization response
        with app.test_request_context():
            with app.session_transaction() as sess:
                sess['oauth_token'] = {'access_token': 'mock-token'}
            response = self.app.get('/authorize')
            self.assertEqual(response.status_code, 302)
            self.assertIn('Location', response.headers)
            self.assertEqual(response.headers['Location'], '/')

if __name__ == '__main__':
    unittest.main()