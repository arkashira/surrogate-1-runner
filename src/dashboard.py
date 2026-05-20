from session_manager import SessionManager
from flask import Flask, jsonify, request

app = Flask(__name__)
session_manager = SessionManager(timeout_minutes=30)

@app.route('/sessions', methods=['GET'])
def get_sessions():
    active_sessions = session_manager.get_active_sessions()
    return jsonify(active_sessions)

@app.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    session = session_manager.get_session(session_id)
    if session:
        return jsonify(session)
    return jsonify({'error': 'Session not found'}), 404

@app.route('/sessions/<session_id>/activity', methods=['POST'])
def update_activity(session_id):
    session_manager.update_activity(session_id)
    return jsonify({'status': 'success'})

@app.route('/sessions/<session_id>/terminate', methods=['POST'])
def terminate_session(session_id):
    if session_manager.terminate_session(session_id):
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Session not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)