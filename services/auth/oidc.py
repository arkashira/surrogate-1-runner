import requests
from flask import Flask, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth
import yaml

app = Flask(__name__)
oauth = OAuth(app)

# Load OIDC configuration from auth.yaml
def load_oidc_config():
    with open('/opt/axentx/surrogate-1/config/auth.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config['oidc']

# Configure OIDC provider
def configure_oidc_provider(config):
    oauth.register(
        name='oidc',
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        server_metadata_url=config['issuer'] + '/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = oauth.oidc.parse_id_token(token)
    session['user'] = user
    return redirect('/')

if __name__ == '__main__':
    oidc_config = load_oidc_config()
    configure_oidc_provider(oidc_config)
    app.run()