import unittest
from unittest.mock import Mock
from unittest.mock import patch
from opt.axentx.surrogate-1.auth.oauth import OAuth2Client
from opt.axentx.surrogate-1.auth.providers import OAuth2Provider

class TestOAuth2Provider(unittest.TestCase):
    def test_get_authorization_url(self):
        provider = OAuth2Provider('test', 'client_id', 'client_secret', 'https://example.com/authorize', 'https://example.com/token')
        self.assertEqual(provider.get_authorization_url(), 'https://example.com/authorize?client_id=client_id&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob')

    def test_fetch_token(self):
        provider = OAuth2Provider('test', 'client_id', 'client_secret', 'https://example.com/authorize', 'https://example.com/token')
        with patch('requests_oauthlib.OAuth2Session.fetch_token') as mock_fetch_token:
            mock_fetch_token.return_value = {'access_token': 'token'}
            token = provider.fetch_token('https://example.com/authorize?code=code')
            self.assertEqual(token, {'access_token': 'token'})

    def test_get_access_token(self):
        provider = OAuth2Provider('test', 'client_id', 'client_secret', 'https://example.com/authorize', 'https://example.com/token')
        token = {'access_token': 'token'}
        self.assertEqual(provider.get_access_token(token), 'token')

if __name__ == '__main__':
    unittest.main()