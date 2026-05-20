import requests
from requests_oauthlib import OAuth2Session

class OAuth2Client:
    def __init__(self, client_id, client_secret, authorization_base_url, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.oauth = OAuth2Session(client_id)

    def get_authorization_url(self):
        return self.oauth.authorization_url(self.authorization_base_url)

    def fetch_token(self, authorization_response):
        token = self.oauth.fetch_token(
            self.token_url,
            client_secret=self.client_secret,
            authorization_response=authorization_response
        )
        return token

    def get_access_token(self, token):
        return token['access_token']