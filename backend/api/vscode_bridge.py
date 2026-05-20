
from flask import Blueprint, request, jsonify
from .. import db
from ..models import PracticeSession

vscode_bridge = Blueprint('vscode_bridge', __name__, url_prefix='/api/vscode')

@vscode_bridge.route('/start_practice', methods=['POST'])
def start_practice():
    data = request.get_json()
    user_id = data['user_id']
    new_session = PracticeSession(user_id=user_id, activity='')
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'message': 'Practice session started'}), 201

@vscode_bridge.route('/log_activity', methods=['POST'])
def log_activity():
    data = request.get_json()
    session_id = data['session_id']
    activity = data['activity']
    session = PracticeSession.query.get(session_id)
    if session:
        session.activity += f'\n{activity}'
        db.session.commit()
        return jsonify({'message': 'Activity logged'}), 200
    else:
        return jsonify({'error': 'Session not found'}), 404