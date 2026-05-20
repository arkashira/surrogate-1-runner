from flask import Flask, request, jsonify
import uuid
import logging
from datetime import datetime

app = Flask(__name__)

# In-memory storage for environments (for demo purposes)
environments = {}

# Configure logging
logging.basicConfig(
    filename='env_management.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/api/environments', methods=['POST'])
def create_environment():
    env_id = str(uuid.uuid4())
    environments[env_id] = True
    logging.info(f"Environment created: {env_id}")
    return jsonify({"id": env_id}), 201

@app.route('/api/environments/<env_id>', methods=['DELETE'])
def delete_environment(env_id):
    if env_id in environments:
        del environments[env_id]
        logging.info(f"Environment deleted: {env_id}")
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"error": "Environment not found"}), 404

@app.route('/health')
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)