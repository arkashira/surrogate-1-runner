from flask import Blueprint, request, jsonify
from uuid import uuid4
import jsonschema
from jsonschema import validate

bp = Blueprint('environment_api', __name__)

# In-memory store for simulated environments
environments = {}

# Configuration schema for validation
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "services": {
            "type": "array",
            "items": {"type": "string", "enum": ["s3", "ec2", "rds", "vpc", "iam"]},
            "minItems": 1
        },
        "region": {"type": "string", "default": "us-east-1"},
        "timeout_minutes": {"type": "number", "minimum": 1, "maximum": 60}
    },
    "required": ["services"]
}

@bp.route('/environments', methods=['POST'])
def create_environment():
    try:
        data = request.get_json()
        validate(instance=data, schema=CONFIG_SCHEMA)
        
        env_id = str(uuid4())
        environments[env_id] = {
            "id": env_id,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "config": {
                **data,
                "timeout_minutes": data.get("timeout_minutes", 30)
            }
        }
        
        return jsonify({
            "id": env_id,
            "status": "active",
            "config": environments[env_id]["config"]
        }), 201
        
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": "Invalid configuration", "details": str(e)}), 400

@bp.route('/environments/<env_id>', methods=['GET'])
def get_environment(env_id):
    env = environments.get(env_id)
    if not env:
        return jsonify({"error": "Environment not found"}), 404
        
    return jsonify({
        "id": env_id,
        "status": env["status"],
        "config": env["config"]
    })

# Test endpoint for validation
@bp.route('/test-config', methods=['POST'])
def test_config():
    try:
        data = request.get_json()
        validate(instance=data, schema=CONFIG_SCHEMA)
        return jsonify({"valid": True})
    except jsonschema.exceptions.ValidationError:
        return jsonify({"valid": False})