from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from models import Runbook
from extensions import db

runbooks_bp = Blueprint('runbooks', __name__)
api = Api(runbooks_bp)


class RunbookListResource(Resource):
    """Handle collection-level operations for runbooks."""
    
    def get(self):
        """List all runbooks."""
        runbooks = Runbook.query.all()
        return [{'id': r.id, 'title': r.title, 'content': r.content} for r in runbooks], 200
    
    def post(self):
        """Create a new runbook."""
        data = request.get_json()
        if not data or 'title' not in data:
            return {'message': 'Title is required'}, 400
        
        runbook = Runbook(
            title=data['title'],
            content=data.get('content', '')
        )
        db.session.add(runbook)
        db.session.commit()
        
        return {'id': runbook.id, 'title': runbook.title, 'content': runbook.content}, 201


class RunbookResource(Resource):
    """Handle individual runbook operations."""
    
    def get(self, id):
        """Get a runbook by ID."""
        runbook = Runbook.query.get(id)
        if runbook is None:
            return {'message': 'Runbook not found'}, 404
        return {'id': runbook.id, 'title': runbook.title, 'content': runbook.content}, 200
    
    def delete(self, id):
        """Delete a runbook by ID."""
        runbook = Runbook.query.get(id)
        if runbook is None:
            return {'message': 'Runbook not found'}, 404
        
        db.session.delete(runbook)
        db.session.commit()
        return '', 204


# Register routes
api.add_resource(RunbookListResource, '/')
api.add_resource(RunbookResource, '/<int:id>')