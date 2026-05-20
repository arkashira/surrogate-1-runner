from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/configure', methods=['POST'])
def configure_proxy():
    config_data = request.json
    # Simulate saving the configuration data
    logging.info(f"Received configuration: {config_data}")
    return jsonify({"status": "Configuration updated successfully"}), 200

@app.route('/status', methods=['GET'])
def get_proxy_status():
    # Simulate fetching the current status of the proxy
    status = {"status": "running", "uptime": "1 hour"}
    return jsonify(status), 200

if __name__ == '__main__':
    app.run(debug=True)