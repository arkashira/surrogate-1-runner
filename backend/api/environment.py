from flask import Blueprint, request, jsonify
from .models.environment import Environment
from .services.aws_service import AWSService

api = Blueprint('environment', __name__)

@api.route('/create_environment', methods=['POST'])
def create_environment():
    try:
        data = request.json
        environment = Environment.create(data)
        aws_service = AWSService()
        aws_service.create_practice_environment(environment)

        return jsonify({"message": "Environment creation initiated", "environment_id": environment.id}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/environment_status/<int:environment_id>', methods=['GET'])
def get_environment_status(environment_id):
    try:
        environment = Environment.get_by_id(environment_id)
        if environment.is_ready:
            return jsonify({"status": "ready", "message": "Environment is ready for use"}), 200
        else:
            return jsonify({"status": "pending", "message": "Environment is still being set up"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500