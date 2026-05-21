from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/compliance-status', methods=['GET'])
def compliance_status():
    # Run the CLI hook command for pre-deploy checks
    result = subprocess.run(['./cli-hook', 'pre-deploy'], capture_output=True, text=True)
    if result.returncode == 0:
        status = "Compliant"
    else:
        status = "Non-compliant"
    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)