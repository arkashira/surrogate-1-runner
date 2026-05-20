from flask import Blueprint, request, jsonify, g
from ..models import Project
from ..middleware.ownership import validate_project_ownership
from ..extensions import db

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('/projects', methods=['GET'])
def get_projects():
    """List all projects for the authenticated user."""
    projects = Project.query.filter_by(user_id=g.user.id).all()
    return jsonify([p.to_dict() for p in projects]), 200

@project_blueprint.route('/projects', methods=['POST'])
def create_project():
    """Create a new project for the authenticated user."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    project_name = data.get('name')
    bundle_id = data.get('bundle_id')
    
    if not project_name:
        return jsonify({'error': 'Project name is required'}), 400
    
    project = Project(
        name=project_name,
        bundle_id=bundle_id,
        user_id=g.user.id
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 201

@project_blueprint.route('/projects/<int:project_id>', methods=['DELETE'])
@validate_project_ownership
def delete_project(project_id, project=None):
    """Delete a project (ownership validated by decorator)."""
    if project:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project deleted successfully'}), 200
    
    return jsonify({'error': 'Project not found'}), 404