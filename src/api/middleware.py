from flask import request, jsonify
from functools import wraps
import logging

# Define API key
API_KEY = "your_api_key_here"

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if API key is present in the request
        if 'API-Key' not in request.headers:
            return jsonify({"type": "https://example.com/errors#unauthorized", "title": "Unauthorized", "detail": "Missing API key"}), 401
        
        # Check if API key is valid
        if request.headers['API-Key'] != API_KEY:
            return jsonify({"type": "https://example.com/errors#unauthorized", "title": "Unauthorized", "detail": "Invalid API key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function