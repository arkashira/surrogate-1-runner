from flask import Blueprint, request, jsonify
from backend.services.cloudwatch_client import CloudWatchClient

integrations_bp = Blueprint('integrations', __name__)

@integrations_bp.route('/test-cloudwatch-connection', methods=['POST'])
def test_cloudwatch_connection():
    data = request.json
    access_key = data.get('access_key')
    secret_key = data.get('secret_key')

    if not access_key or not secret_key:
        return jsonify({'success': False, 'message': 'Missing credentials'}), 400

    cloudwatch_client = CloudWatchClient(access_key, secret_key)
    result = cloudwatch_client.test_connection()

    return jsonify(result)