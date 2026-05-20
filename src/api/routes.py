from flask import Flask, jsonify, request
from flask_oauthlib.provider import OAuth2Provider
from functools import wraps
from datetime import datetime, timedelta
import time
import os

app = Flask(__name__)
oauth = OAuth2Provider(app)

# In-memory data for demonstration
spend_data = [
    {
        "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
        "model": f"gpt-4.0-{i}",
        "tokens": 123456 + i * 1000,
        "cost": (0.02 + i * 0.001) * (123456 + i * 1000) / 1_000_000,
        "team": f"team-{i % 5 + 1}"
    }
    for i in range(30)
]

# Mock OAuth2 token validation
@oauth.clientgetter
def load_client(client_id):
    return {'client_id': client_id}

@oauth.grantgetter
def load_grant(client_id, code):
    return {'client_id': client_id, 'code': code}

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    return {'access_token': access_token}

# Rate limiting decorator with user identification
def rate_limit(limit=1000, period=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = request.headers.get('Authorization').split()[1]  # Extract user ID from token
            key = f'{user_id}:{request.path}'
            now = int(time.time())
            if not hasattr(decorated_function, 'calls'):
                decorated_function.calls = {}
            calls = decorated_function.calls.get(key, [])
            calls = [call for call in calls if call > now - period]
            if len(calls) >= limit:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            calls.append(now)
            decorated_function.calls[key] = calls
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/finance/spend', methods=['GET'])
@oauth.require_oauth()
@rate_limit(limit=1000, period=60)
def get_spend():
    return jsonify(spend_data)

if __name__ == '__main__':
    app.run(debug=True)