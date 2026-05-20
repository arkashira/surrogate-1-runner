import time
from flask import Flask, jsonify

app = Flask(__name__)

# Simulated device ID registration
device_id = None

def register_device():
    global device_id
    # Simulate registration with surrogate-1
    time.sleep(1)  # Simulate network delay
    device_id = "unique-device-id"  # Replace with actual device ID logic

@app.route('/health-check', methods=['GET'])
def health_check():
    if device_id is None:
        return jsonify({"status": "not ready"}), 503
    return jsonify({"status": "ok", "device_id": device_id}), 200

if __name__ == '__main__':
    register_device()
    time.sleep(5)  # Ensure agent starts within 5 seconds
    app.run(host='0.0.0.0', port=5000)