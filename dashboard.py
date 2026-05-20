
from flask import Flask, render_template, jsonify, request
import logging
from axentx_api.client import AxentxApiClient

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_client = AxentxApiClient()

@app.route('/')
def index():
    """Render the main dashboard page."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        
        detections = api_client.get_signature_drift_detections(
            page=page, 
            per_page=per_page
        )
        return render_template('dashboard.html', detections=detections)
    except Exception as e:
        logger.error(f"Error fetching detections: {e}")
        return render_template('error.html', error=str(e)), 500

@app.route('/api/detections')
def api_detections():
    """JSON endpoint for real-time polling."""
    try:
        detections = api_client.get_signature_drift_detections(limit=50)
        return jsonify({'detections': detections, 'count': len(detections)})
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Never use debug=True in production