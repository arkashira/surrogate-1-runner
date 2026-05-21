from flask import Blueprint, jsonify
from datetime import datetime

validation_bp = Blueprint('validation', __name__, url_prefix='/api/validation')

# Mock data store
PROJECTS = [
    {
        "id": 1,
        "name": "Project Alpha",
        "created_at": datetime(2026, 5, 1, 12, 0).isoformat(),
        "progress": 45,
        "status": "InProgress",
    },
    {
        "id": 2,
        "name": "Project Beta",
        "created_at": datetime(2026, 5, 2, 9, 30).isoformat(),
        "progress": 100,
        "status": "Completed",
    },
]

@validation_bp.route('/projects')
def get_projects():
    return jsonify(PROJECTS)