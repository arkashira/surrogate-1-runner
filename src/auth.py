import hmac
from functools import wraps
from flask import request, jsonify

def token_required(f):
    """Simple bearer‑token authentication decorator with timing-safe comparison."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        parts = auth.split()
        
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Unauthorized"}), 401
        
        # Timing-safe comparison
        from .config import API_TOKEN
        if not hmac.compare_digest(parts[1], API_TOKEN):
            return jsonify({"error": "Unauthorized"}), 401
            
        return f(*args, **kwargs)
    return decorated