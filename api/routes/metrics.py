from flask import Blueprint, jsonify
from .models import AlertMetrics

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = AlertMetrics.get_latest()
    return jsonify({
        'total_alerts_received': metrics.total_alerts_received,
        'alerts_consolidated': metrics.alerts_consolidated,
        'noise_alerts_identified': metrics.noise_alerts_identified,
        'reduction_percentage': metrics.reduction_percentage
    })

class AlertMetrics:
    @staticmethod
    def get_latest():
        # Placeholder for actual database query logic
        return {
            'total_alerts_received': 1000,
            'alerts_consolidated': 800,
            'noise_alerts_identified': 150,
            'reduction_percentage': 0.85
        }