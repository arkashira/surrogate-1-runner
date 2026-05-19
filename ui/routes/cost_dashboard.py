from flask import Blueprint, render_template, request
from flask import jsonify
from datetime import datetime, timedelta
import random

cost_dashboard_bp = Blueprint('cost_dashboard', __name__)

@cost_dashboard_bp.route('/ui/costs', methods=['GET'])
def cost_dashboard():
    anomalies = get_recent_anomalies()
    forecast_data = get_forecast_data()
    return render_template('cost_dashboard.html', anomalies=anomalies, forecast_data=forecast_data)

def get_recent_anomalies():
    # Simulating fetching anomalies from the last 7 days
    return [
        {"date": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'), 
         "severity": random.choice(['low', 'medium', 'high'])} for i in range(7)
    ]

def get_forecast_data():
    # Simulating forecast data for 30 days
    return {
        "dates": [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)],
        "forecast": [random.uniform(100, 500) for _ in range(30)],
        "actual": [random.uniform(100, 500) for _ in range(30)],
    }