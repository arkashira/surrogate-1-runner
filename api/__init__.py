from flask import Flask, jsonify, request, g
from prometheus_client import make_wsgi_app
from .metrics import (
    record_request_duration,
    record_error,
    record_health_check,
    get_metrics
)

app = Flask(__name__)

# Enable Prometheus metrics endpoint
@app.route('/metrics')
def metrics():
    return get_metrics(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# Middleware to instrument all requests
@app.before_request
def before_request():
    g.start_time = None
    g.endpoint = request.endpoint or request.path

@app.after_request
def after_request(response):
    if g.start_time is not None:
        duration = (
            request.environ.get('REQUEST_TIME_FLOAT', 0) - g.start_time
        )
        endpoint = g.endpoint or request.path
        record_request_duration(endpoint, duration)
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    endpoint = request.endpoint or request.path
    record_error(endpoint, 500)
    return jsonify({'error': str(e)}), 500

# ROI endpoint
@app.route('/roi', methods=['GET', 'POST'])
def roi():
    """ROI calculation endpoint."""
    g.start_time = request.environ.get('REQUEST_TIME_FLOAT', 0)
    try:
        if request.method == 'GET':
            return jsonify({'status': 'ok', 'data': {'roi': 0.0}})
        elif request.method == 'POST':
            data = request.get_json() or {}
            roi_value = data.get('value', 0.0)
            return jsonify({'status': 'ok', 'data': {'roi': roi_value}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Recommend endpoint
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Recommendation endpoint."""
    g.start_time = request.environ.get('REQUEST_TIME_FLOAT', 0)
    try:
        if request.method == 'GET':
            return jsonify({'status': 'ok', 'data': {'recommendations': []}})
        elif request.method == 'POST':
            data = request.get_json() or {}
            recommendations = data.get('items', [])
            return jsonify({'status': 'ok', 'data': {'recommendations': recommendations}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    record_health_check('healthy')
    return jsonify({'status': 'healthy', 'service': 'surrogate-1-api'}), 200

# WSGI app for Prometheus integration
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)