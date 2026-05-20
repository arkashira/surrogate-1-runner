from flask import request, jsonify
from functools import wraps

API_KEYS = {"your_api_key_1", "your_api_key_2"}  # Replace with actual API keys

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key or api_key not in API_KEYS:
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function