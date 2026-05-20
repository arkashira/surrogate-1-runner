from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from .services.forecast_service import get_forecast

forecast_bp = Blueprint('forecast', __name__)

@forecast_bp.route('/forecast', methods=['GET'])
def forecast():
    try:
        # Get the forecast for the next 7 days
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        forecast_data = get_forecast(start_date, end_date)

        return jsonify({
            'status': 'success',
            'data': forecast_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500