from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import uuid
import os

app = Flask(__name__)

# Dummy data structure for demonstration purposes
analytics_data = {
    'gpu_utilization': [50, 60, 70],
    'bandwidth': [100, 150, 200],
    'fps': [30, 35, 40]
}

shared_reports = {}

@app.route('/generate_report', methods=['POST'])
def generate_report():
    report_id = str(uuid.uuid4())
    expiration_date = datetime.now() + timedelta(days=7)
    shared_reports[report_id] = {
        'data': analytics_data,
        'expiration': expiration_date
    }
    return jsonify({'report_id': report_id}), 200

@app.route('/get_report/<report_id>', methods=['GET'])
def get_report(report_id):
    if report_id not in shared_reports:
        return jsonify({'error': 'Report not found'}), 404
    
    report = shared_reports[report_id]
    
    if datetime.now() > report['expiration']:
        del shared_reports[report_id]
        return jsonify({'error': 'Report expired'}), 403
    
    return jsonify(report['data']), 200

if __name__ == '__main__':
    app.run(debug=True)