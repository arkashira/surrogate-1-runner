class OAuth2Provider:
    def __init__(self, name, client_id, client_secret, authorization_base_url, token_url):
        self.name = name
        self.oauth_client = OAuth2Client(
            client_id,
            client_secret,
            authorization_base_url,
            token_url
        )

    def get_authorization_url(self):
        return self.oauth_client.get_authorization_url()

    def fetch_token(self, authorization_response):
        return self.oauth_client.fetch_token(authorization_response)

    def get_access_token(self, token):
        return self.oauth_client.get_access_token(token)