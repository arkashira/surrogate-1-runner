
from flask import Flask, request, jsonify
from uuid import uuid4
from src.main.metrics_store import MetricsStore

app = Flask(__name__)
metrics_store = MetricsStore()

@app.route('/api/v1/events', methods=['POST'])
def send_event():
    data = request.get_json()
    event_id = str(uuid4())
    # Process event data and store it or send it to other systems
    # For now, just return a mock event ID
    return jsonify({'event_id': event_id}), 200

@app.route('/api/v1/series', methods=['POST'])
def send_metric():
    data = request.get_json()
    metric_type = data.get('type')
    metric_name = data.get('metric')
    value = data.get('value')

    if metric_type not in ['count', 'gauge', 'timer']:
        return jsonify({'error': 'Unsupported metric type'}), 400

    metrics_store.store_metric(metric_name, metric_type, value)
    return jsonify({'status': 'ok'}), 200

@app.route('/api/v1/series', methods=['GET'])
def get_metrics():
    metric = request.args.get('metric')
    if not metric:
        return jsonify({'error': 'Missing metric parameter'}), 400

    metrics = metrics_store.get_metrics(metric)
    return jsonify(metrics), 200

if __name__ == '__main__':
    app.run(debug=True)