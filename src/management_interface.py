from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/manage', methods=['POST'])
def manage_proxy():
    action = request.json.get('action')
    if action == 'start':
        logging.info("Starting the proxy...")
        return jsonify({"status": "Proxy started"}), 200
    elif action == 'stop':
        logging.info("Stopping the proxy...")
        return jsonify({"status": "Proxy stopped"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400

@app.route('/logs', methods=['GET'])
def get_proxy_logs():
    # Simulate fetching logs
    logs = ["Log entry 1", "Log entry 2"]
    return jsonify({"logs": logs}), 200

if __name__ == '__main__':
    app.run(debug=True)