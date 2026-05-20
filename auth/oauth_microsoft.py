
import os
import requests
from authlib.integrations.base_client import OAuthError
from .base import OAuthProvider
from ..models import User
from ..utils import encrypt_data, decrypt_data

class MicrosoftOAuth(OAuthProvider):
    name = 'microsoft'
    authorize_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    scope = ['openid', 'profile', 'email', 'https://graph.microsoft.com/.default']

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorize_url(self, redirect_uri, state, **kwargs):
        return self.authorize_url + f"?client_id={self.client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}&scope={'+'.join(self.scope)}&response_mode=query"

    def parse_authorize_response(self, data):
        return {
            'access_token': data['access_token'],
            'refresh_token': data['refresh_token'],
            'id_token': data['id_token'],
            'token_type': data['token_type'],
            'expires_in': data['expires_in'],
            'scope': data['scope'],
            'user_info': self.get_user_info(data['access_token']),
        }

    def get_user_info(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        return response.json()

    def get_access_token(self, code, redirect_uri):
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': '+'.join(self.scope),
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code != 200:
            raise OAuthError(f'Failed to obtain access token: {response.text}')
        return response.json()['access_token']

    def store_token(self, user, access_token, refresh_token):
        user.access_token = encrypt_data(access_token)
        user.refresh_token = encrypt_data(refresh_token)
        user.save()

    def retrieve_token(self, user):
        return decrypt_data(user.access_token), decrypt_data(user.refresh_token)

    def get_word_files(self, user):
        access_token, _ = self.retrieve_token(user)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://graph.microsoft.com/v1.0/me/drive/root/children', headers=headers)
        if response.status_code != 200:
            return []
        files = [item['name'] for item in response.json()['value'] if item['folder'] == False]
        return files

    def retry_token(self, user):
        _, refresh_token = self.retrieve_token(user)
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': '+'.join(self.scope),
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code != 200:
            return None
        return response.json()['access_token']

# /opt/axentx/surrogate-1/api/routes.py

from flask import Blueprint, jsonify, request
from . import db
from ..auth import MicrosoftOAuth
from ..models import User

microsoft = Blueprint('microsoft', __name__)

@microsoft.route('/api/microsoft/docs')
def get_word_files():
    user = User.query.get(1)  # Replace 1 with the current user's ID
    oauth = MicrosoftOAuth(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
    files = oauth.get_word_files(user)
    return jsonify(files)

# /opt/axentx/surrogate-1/templates/index.html

<!-- ... -->
<div class="container">
  <h1>Connect Microsoft 365</h1>
  <a href="{{ url_for('microsoft.authorize') }}">Connect with Microsoft</a>
  {% if error %}
    <p style="color: red;">{{ error }}</p>
  {% endif %}
</div>
<!-- ... -->

# Summary
- Added Microsoft OAuth endpoint in `/opt/axentx/surrogate-1/auth/oauth_microsoft.py`
- Added route to get Word files in `/opt/axentx/surrogate-1/api/routes.py`
- Updated index page to include Microsoft connection button in `/opt/axentx/surrogate-1/templates/index.html`
- Implemented Microsoft OAuth flow analogously to Google
- Stored access token encrypted in the same user model
- Implemented endpoint `/api/microsoft/docs` to return a list of the user’s Word files
- Added clear retry option for failure to obtain a token