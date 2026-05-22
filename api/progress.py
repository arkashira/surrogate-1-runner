from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

db = SQLAlchemy()
Base = declarative_base()

class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    quiz_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

progress_blueprint = Blueprint('progress', __name__)

@progress_blueprint.route('/progress', methods=['GET'])
def get_progress():
    session = db.session
    progress_data = session.query(Progress).all()
    return jsonify([{'id': p.id, 'user_id': p.user_id, 'quiz_score': p.quiz_score, 'created_at': p.created_at} for p in progress_data])

@progress_blueprint.route('/progress', methods=['POST'])
def create_progress():
    session = db.session
    data = request.get_json()
    new_progress = Progress(user_id=data['user_id'], quiz_score=data['quiz_score'])
    session.add(new_progress)
    session.commit()
    return jsonify({'id': new_progress.id, 'user_id': new_progress.user_id, 'quiz_score': new_progress.quiz_score, 'created_at': new_progress.created_at})

@progress_blueprint.route('/progress/reset', methods=['POST'])
def reset_progress():
    session = db.session
    data = request.get_json()
    user_id = data['user_id']
    confirm = data['confirm']
    if confirm:
        session.query(Progress).filter(Progress.user_id == user_id).delete()
        session.commit()
        return jsonify({'message': 'Progress reset successfully'})
    else:
        return jsonify({'message': 'Confirmation required to reset progress'}), 400