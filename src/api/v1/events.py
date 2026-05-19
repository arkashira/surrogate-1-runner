from flask import Blueprint, request, jsonify
from datetime import datetime
import pytz

events_bp = Blueprint('events', __name__)

def validate_event(data):
    errors = []

    if not all(isinstance(data.get(field), str) for field in ['title', 'text']):
        errors.append({'field': 'title,text', 'message': 'Title and Text are required and must be strings'})

    if 'timestamp' in data and not isinstance(data['timestamp'], str):
        errors.append({'field': 'timestamp', 'message': 'Timestamp must be a valid ISO 8601 string'})

    return errors

def normalize_timestamp(timestamp_str):
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        timestamp = timestamp.astimezone(pytz.UTC)
        return timestamp.isoformat()
    except ValueError:
        return None

@events_bp.route('/events', methods=['POST'])
def post_event():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        return jsonify({
            'status': 'error',
            'code': 400,
            'errors': [{'field': 'body', 'message': 'Request body must be a valid JSON object'}]
        }), 400

    errors = validate_event(data)

    if errors:
        return jsonify({
            'status': 'error',
            'code': 400,
            'errors': errors
        }), 400

    if 'timestamp' in data:
        normalized_timestamp = normalize_timestamp(data['timestamp'])
        if normalized_timestamp is None:
            return jsonify({
                'status': 'error',
                'code': 400,
                'errors': [{'field': 'timestamp', 'message': 'Invalid timestamp format. Use ISO 8601 format.'}]
            }), 400
        data['timestamp'] = normalized_timestamp

    return jsonify({
        'status': 'ok',
        'event': data
    }), 202