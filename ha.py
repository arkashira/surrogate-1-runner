import os
import time
from flask import Flask, jsonify
import redis  # For dataset store health check

app = Flask(__name__)

def is_dataset_store_healthy():
    """Check health by verifying connection to the dataset store."""
    try:
        # Connect to the dataset store (e.g., Redis or DB)
        r = redis.Redis(host='dataset-store', port=6379, db=0, socket_timeout=1)
        r.ping()  # Should return True if healthy
        return True
    except Exception as e:
        print(f"Dataset store health check failed: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Expose health status endpoint."""
    if is_dataset_store_healthy():
        return jsonify({"status": "healthy", "message": "Dataset store reachable"}), 200
    else:
        return jsonify({"status": "unhealthy", "message": "Dataset store unreachable"}), 503

if __name__ == '__main__':
    # Run health check server on all interfaces at port 8080
    app.run(host='0.0.0.0', port=8080, debug=False)