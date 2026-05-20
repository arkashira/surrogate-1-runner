from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import db, UserEvent

events_bp = Blueprint('events', __name__)

@events_bp.route('/api/events', methods=['POST'])
def post_event():
    data = request.json
    required_fields = ['user_id', 'event_type']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user_id = data['user_id']
    event_type = data['event_type']
    payload = data.get('payload', None)

    event = UserEvent(
        user_id=user_id,
        event_type=event_type,
        payload=payload,
        timestamp=datetime.utcnow()
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event recorded successfully"}), 201