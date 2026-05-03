from flask import request, jsonify
from events import RequestCreatedEvent
from internal_event_bus import emit_event

@app.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    required_fields = ['type', 'title', 'owner', 'sla_target']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate SLA target
    try:
        sla_target = datetime.strptime(data['sla_target'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid SLA target'}), 422
    
    # Create request
    request_id = db.create_request(data['type'], data['title'], data['owner'], sla_target)
    
    # Emit request.created event
    event = RequestCreatedEvent(request_id, data['type'], data['title'], data['owner'], data['sla_target'])
    emit_event('request.created', event)
    
    return jsonify({'request_id': request_id}), 201