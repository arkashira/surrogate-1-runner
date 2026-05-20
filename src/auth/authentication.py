import logging
from functools import wraps
from typing import Any, Callable
from flask import request, jsonify, session
from werkzeug.exceptions import Unauthorized, Forbidden

logger = logging.getLogger(__name__)

# Mock user database - in reality this would connect to a real DB
USERS = {
    'admin': {'password': 'admin_pass', 'role': 'administrator'},
    'analyst': {'password': 'analyst_pass', 'role': 'analyst'},
    'user': {'password': 'user_pass', 'role': 'user'}
}

ROLES_PERMISSIONS = {
    'administrator': ['read', 'write', 'delete'],
    'analyst': ['read', 'write'],
    'user': ['read']
}

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user against the mock database."""
    user = USERS.get(username)
    if not user:
        return False
    return user['password'] == password

def get_current_user() -> dict:
    """Get current user from session."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return USERS.get(user_id)

def require_auth(f: Callable) -> Callable:
    """Decorator to require authentication for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not session.get('user_id'):
            logger.warning("Unauthorized access attempt - no session found")
            raise Unauthorized("Authentication required")
        
        # Get current user
        user = get_current_user()
        if not user:
            logger.warning("Unauthorized access attempt - invalid session user")
            raise Unauthorized("Invalid session")
            
        return f(*args, **kwargs)
    return decorated_function

def require_permission(permission: str) -> Callable:
    """Decorator to require a specific permission level."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Ensure user is authenticated first
            user = get_current_user()
            if not user:
                logger.warning("Permission check failed - no authenticated user")
                raise Unauthorized("Authentication required")
            
            # Check if user has required permission
            role = user['role']
            permissions = ROLES_PERMISSIONS.get(role, [])
            
            if permission not in permissions:
                logger.warning(f"Access denied - user {user['username']} lacks permission {permission}")
                raise Forbidden(f"Insufficient permissions for {permission}")
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login(username: str, password: str) -> bool:
    """Handle user login."""
    if authenticate_user(username, password):
        session['user_id'] = username
        logger.info(f"User {username} logged in successfully")
        return True
    else:
        logger.warning(f"Failed login attempt for user {username}")
        return False

def logout():
    """Handle user logout."""
    session.pop('user_id', None)
    logger.info("User logged out")

def init_auth(app):
    """Initialize authentication with Flask app."""
    @app.before_request
    def check_authentication():
        # Skip auth for login endpoint
        if request.endpoint == 'login':
            return
        
        # Skip auth for static files
        if request.endpoint and 'static' in request.endpoint:
            return
            
        # Require authentication for all other routes
        if not session.get('user_id'):
            raise Unauthorized("Authentication required")