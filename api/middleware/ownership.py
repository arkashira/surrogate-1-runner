from flask import request, jsonify, g
from functools import wraps
from ..models import Project
from ..extensions import db

def validate_project_ownership(func):
    """
    Decorator to validate that the current user owns the project.
    Must be used after authentication middleware (which sets g.user).
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        project_id = kwargs.get('project_id')
        
        if not project_id:
            return jsonify({'error': 'Project ID required'}), 400
        
        # Use modern SQLAlchemy (get_or_404 or session.get)
        project = db.session.get(Project, project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Ownership check
        if project.user_id != g.user.id:
            return jsonify({'error': 'Forbidden: Project does not belong to current user'}), 403
        
        # Attach project to kwargs for route handler convenience
        kwargs['project'] = project
        return func(*args, **kwargs)
    
    return wrapper