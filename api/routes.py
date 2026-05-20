from flask import Blueprint, request, jsonify
from surrogate_1.api.middleware import validate_permissions

routes = Blueprint('routes', __name__)

@routes.route('/session', methods=['GET'])
@validate_permissions
def get_session():
    session_id = request.args.get('session_id')
    # Return the session data
    return jsonify({'session_id': session_id})

@routes.route('/session/permissions', methods=['POST'])
def set_permissions():
    session_id = request.json['session_id']
    user_id = request.json['user_id']
    # Add or remove the user from the session's permissions list
    permission = db.session.query(Permission).filter_by(session_id=session_id, user_id=user_id).first()
    if permission:
        db.session.delete(permission)
    else:
        new_permission = Permission(session_id=session_id, user_id=user_id)
        db.session.add(new_permission)
    db.session.commit()
    return jsonify({'message': 'Permissions updated'})