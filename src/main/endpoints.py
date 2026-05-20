from flask import Flask, request, jsonify
import uuid
from .metrics_store import MetricsStore

app = Flask(__name__)
metrics_store = MetricsStore()

@app.route('/api/v1/events', methods=['POST'])
def post_event():
    event_data = request.json
    mock_event_id = str(uuid.uuid4())
    return jsonify({"event_id": mock_event_id}), 200

@app.route('/api/v1/series', methods=['POST'])
def post_metric():
    metric_data = request.json
    metric_name = metric_data.get('metric')
    metric_type = metric_data.get('type')
    metric_value = metric_data.get('value')

    if not all([metric_name, metric_type, metric_value]):
        return jsonify({"error": "Invalid metric data"}), 400

    metrics_store.store_metric(metric_name, metric_type, metric_value)
    return jsonify({"status": "Metric stored"}), 200

@app.route('/api/v1/series', methods=['GET'])
def get_metrics():
    metric_name = request.args.get('metric')
    if not metric_name:
        return jsonify({"error": "Metric name is required"}), 400

    metrics = metrics_store.query_metrics(metric_name)
    return jsonify(metrics), 200

if __name__ == '__main__':
    app.run(debug=True)