import logging
from functools import wraps
from flask import request, jsonify
from surrogate_1_sdk import API_KEY_HEADER  # Use SDK constant for consistency
from surrogate_1.utils.api_key_validator import validate_api_key

logger = logging.getLogger(__name__)

def authentication_middleware(func):
    """Auth middleware with backward compatibility for v0.9.x APIs."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Backward compatibility: skip auth for v0.9.x clients
        api_version = request.headers.get('X-API-Version', '').startswith('0.9')
        if api_version:
            logger.debug("Bypassing auth for v0.9.x compatible request")
            return func(*args, **kwargs)
        
        # Check for API key
        api_key = request.headers.get(API_KEY_HEADER)
        if not api_key:
            logger.warning("Request missing required API key")
            return jsonify({"error": "Authentication required. Provide API key in X-API-Key header."}), 401
        
        # Validate against existing API key system
        if not validate_api_key(api_key):
            logger.warning(f"Invalid API key attempt: {api_key[:8]}...")
            return jsonify({"error": "Invalid API key"}), 401
        
        logger.debug("Authentication successful")
        return func(*args, **kwargs)
    return wrapper