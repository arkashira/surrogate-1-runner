
import os
import jwt
from datetime import datetime, timedelta
from flask import request

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

def get_token_from_request():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        return token
    return None

# opt/axentx/surrogate-1/backend/api.py

from flask import Flask, request, jsonify
from auth.token import generate_token, verify_token, get_token_from_request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.json.get('user_id')
    if user_id:
        token = generate_token(user_id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'User ID not provided'}), 400

@app.route('/protected', methods=['GET'])
def protected():
    token = get_token_from_request()
    if token:
        payload = verify_token(token)
        if isinstance(payload, dict):
            return jsonify({'message': 'Access granted', 'user_id': payload['user_id']}), 200
        else:
            return jsonify({'message': payload}), 401
    return jsonify({'message': 'Token not provided'}), 401

## Summary
- Implemented token generation and verification functions in `token.py`.
- Updated `api.py` to include routes for login and protected resource access.
- Token is now handled and verified for extension calls.