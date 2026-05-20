from flask import Blueprint, jsonify
from datetime import datetime
from collections import defaultdict

consolidated_bp = Blueprint('consolidated', __name__)

# Mock data for demonstration purposes
ALERTS_DATA = [
    {"title": "High CPU Usage", "service": "ServiceA", "severity": "critical", "timestamp": datetime(2023, 10, 1, 12, 0)},
    {"title": "Disk Space Low", "service": "ServiceB", "severity": "warning", "timestamp": datetime(2023, 10, 2, 14, 0)},
    {"title": "Memory Leak Detected", "service": "ServiceA", "severity": "info", "timestamp": datetime(2023, 10, 3, 16, 0)},
    # Additional mock alerts can be added here
]

@consolidated_bp.route('/api/consolidated_alerts', methods=['GET'])
def get_consolidated_alerts():
    consolidated_groups = defaultdict(lambda: {"alert_count": 0, "first_seen": None, "last_seen": None, "service": None})

    for alert in ALERTS_DATA:
        key = (alert['title'], alert['service'])
        consolidated_groups[key]['alert_count'] += 1
        consolidated_groups[key]['service'] = alert['service']
        consolidated_groups[key]['first_seen'] = min(consolidated_groups[key]['first_seen'], alert['timestamp']) if consolidated_groups[key]['first_seen'] else alert['timestamp']
        consolidated_groups[key]['last_seen'] = max(consolidated_groups[key]['last_seen'], alert['timestamp']) if consolidated_groups[key]['last_seen'] else alert['timestamp']
    
    sorted_groups = sorted(consolidated_groups.items(), key=lambda x: (severity_order(x[0][0]), x[1]['alert_count']), reverse=True)

    response = [
        {
            "title": group[0][0],
            "service": group[1]['service'],
            "alert_count": group[1]['alert_count'],
            "first_seen": group[1]['first_seen'].isoformat(),
            "last_seen": group[1]['last_seen'].isoformat()
        }
        for group in sorted_groups
    ][:1000]  # Limit to 1000 groups

    return jsonify(response)

def severity_order(severity):
    order = {"critical": 3, "warning": 2, "info": 1}
    return order.get(severity, 0)