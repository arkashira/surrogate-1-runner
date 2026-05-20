from flask import request, jsonify
from functools import wraps
from surrogate_1 import app, db

def validate_permissions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        session_id = request.args.get('session_id')
        user_id = request.args.get('user_id')
        
        # Check if user has permission to access the session
        if not has_permission(session_id, user_id):
            return jsonify({'error': 'Permission denied'}), 403
        
        return func(*args, **kwargs)
    
    return decorated_function

def has_permission(session_id, user_id):
    # Query the database to check if the user has permission to access the session
    session = db.session.query(Session).filter_by(id=session_id).first()
    if session and session.owner_id == user_id:
        return True
    
    # Check if the user is in the session's permissions list
    permissions = db.session.query(Permission).filter_by(session_id=session_id, user_id=user_id).first()
    if permissions:
        return True
    
    return False

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    permissions = db.relationship('Permission', backref='session', lazy=True)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sessions = db.relationship('Session', backref='owner', lazy=True)
    permissions = db.relationship('Permission', backref='user', lazy=True)