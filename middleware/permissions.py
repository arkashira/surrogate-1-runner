from functools import wraps
from flask import request, jsonify

# Define access levels
ACCESS_LEVELS = {
    'admin': 3,
    'engineer': 2,
    'read-only': 1
}

# Mock user data for demonstration purposes
USER_DATA = {
    'user1': 'admin',
    'user2': 'engineer',
    'user3': 'read-only'
}

def get_user_access_level(username):
    """Retrieve the access level for a given username."""
    return USER_DATA.get(username, None)

def permission_required(required_level):
    """Decorator to enforce access level permissions."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            username = request.headers.get('X-Username')
            user_access_level = get_user_access_level(username)

            if user_access_level is None:
                return jsonify({'error': 'User not found'}), 403
            
            if ACCESS_LEVELS[user_access_level] < ACCESS_LEVELS[required_level]:
                return jsonify({'error': 'Access denied'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Example usage of the middleware
# from flask import Flask
# app = Flask(__name__)

# @app.route('/admin', methods=['GET'])
# @permission_required('admin')
# def admin_route():
#     return jsonify({'message': 'Welcome, admin!'})

# @app.route('/protected', methods=['GET'])
# @permission_required('engineer')
# def protected_route():
#     return jsonify({'message': 'You have access to this route!'})