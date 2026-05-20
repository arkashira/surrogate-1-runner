from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock database for support requests
support_requests = []

@app.route('/support', methods=['POST'])
def submit_support_request():
    data = request.get_json()
    if not data or 'issue' not in data:
        return jsonify({'error': 'Issue description is required'}), 400

    support_request = {
        'id': len(support_requests) + 1,
        'issue': data['issue'],
        'status': 'open',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    support_requests.append(support_request)
    return jsonify(support_request), 201

@app.route('/support/<int:request_id>', methods=['GET'])
def get_support_request(request_id):
    request = next((req for req in support_requests if req['id'] == request_id), None)
    if not request:
        return jsonify({'error': 'Support request not found'}), 404
    return jsonify(request)

@app.route('/support/<int:request_id>', methods=['PUT'])
def update_support_request(request_id):
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400

    request = next((req for req in support_requests if req['id'] == request_id), None)
    if not request:
        return jsonify({'error': 'Support request not found'}), 404

    request['status'] = data['status']
    request['updated_at'] = datetime.now().isoformat()
    return jsonify(request)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    if not data or 'feedback' not in data:
        return jsonify({'error': 'Feedback is required'}), 400

    feedback = {
        'id': len(support_requests) + 1,
        'feedback': data['feedback'],
        'created_at': datetime.now().isoformat()
    }
    support_requests.append(feedback)
    return jsonify(feedback), 201

if __name__ == '__main__':
    app.run(debug=True)