from flask import Blueprint, jsonify, request
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

forecast_blueprint = Blueprint('forecast', __name__)

@forecast_blueprint.route('/forecast', methods=['GET'])
def get_forecast():
    try:
        # Load historical data (last 90 days) from a configurable file path
        data_path = request.args.get('data_path', default='historical_data.csv')
        data = pd.read_csv(data_path, index_col='date', parse_dates=True)

        # Validate data integrity
        if data.isnull().values.any():
            logging.error("Invalid data: missing values detected")
            return jsonify({"error": "Invalid data"}), 400

        # Fit ARIMA model
        model = ARIMA(data, order=(5,1,0))
        model_fit = model.fit()

        # Make prediction for next 30 days
        forecast = model_fit.forecast(steps=30)

        # Calculate confidence interval (assuming 95% confidence)
        conf_interval = 1.96 * sqrt(mean_squared_error(data, model_fit.fittedvalues))

        # Prepare response
        response = []
        for i in range(30):
            response.append({
                'date': data.index[-1] + pd.Timedelta(days=i+1),
                'predicted_cost': forecast[i],
                'confidence_interval': conf_interval
            })

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500