import os
import json
from flask import Flask, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

app = Flask(__name__)

# Load mappings from environment variable or default to an empty dictionary
MAPPINGS = {}
try:
    mappings_json = os.environ.get('SERVICE_MAPPINGS', '{}')
    MAPPINGS = json.loads(mappings_json)
except json.JSONDecodeError:
    print("Invalid JSON format in SERVICE_MAPPINGS. Using empty dictionary.")

# Load authentication token from environment variable or use a default
AUTH_TOKEN = os.environ.get('API_AUTH_TOKEN', 'default-token')

def authenticate():
    """Authenticate request using static token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise Unauthorized("Missing or invalid Authorization header")
    token = auth_header.split(' ')[1]
    if token != AUTH_TOKEN:
        raise Unauthorized("Invalid token")
    return True

@app.route('/api/v1/mappings', methods=['GET'])
def get_mappings():
    """Return current mappings in JSON"""
    authenticate()
    return jsonify(MAPPINGS)

@app.route('/api/v1/mappings', methods=['POST'])
def add_mapping():
    """Add a new mapping and return 201"""
    authenticate()
    data = request.get_json()
    if not data or 'service_name' not in data or 'target_url' not in data:
        raise BadRequest("Invalid payload. Missing 'service_name' or 'target_url'")

    service_name = data['service_name']
    target_url = data['target_url']

    # Add mapping and trigger hot-reload
    MAPPINGS[service_name] = target_url
    trigger_hot_reload()

    return jsonify({'service_name': service_name, 'target_url': target_url}), 201

@app.route('/api/v1/mappings/<string:service_name>', methods=['DELETE'])
def delete_mapping(service_name):
    """Remove the mapping and return 204"""
    authenticate()
    if service_name not in MAPPINGS:
        raise NotFound("Service not found")

    del MAPPINGS[service_name]
    trigger_hot_reload()

    return '', 204

def trigger_hot_reload():
    """Trigger hot-reload mechanism"""
    # In a real implementation, this might:
    # - Signal to the main application to reload config
    # - Write updated config to disk
    # - Send signal to worker processes
    print("Hot-reload triggered")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)