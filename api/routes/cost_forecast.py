from flask import Blueprint, request, jsonify
import pandas as pd
from fbprophet import Prophet
import numpy as np
import datetime
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Create a blueprint for the cost forecast
cost_forecast_bp = Blueprint('cost_forecast', __name__)

# Mock function to simulate fetching historical data
def fetch_historical_data(provider):
    # This function should return a DataFrame with 'date' and 'amount_usd' columns
    # Here we simulate it with random data for demonstration purposes
    dates = pd.date_range(end=datetime.datetime.now(), periods=180).tolist()
    amounts = np.random.rand(180) * 1000  # Simulated spend amounts
    return pd.DataFrame({'date': dates, 'amount_usd': amounts})

# Function to create a forecast using Prophet
def create_forecast(data):
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].rename(columns={'ds': 'date', 'yhat': 'amount_usd'})

@cost_forecast_bp.route('/v1/costs/forecast', methods=['GET'])
def get_cost_forecast():
    provider = request.args.get('provider')
    if provider not in ['aws', 'gcp', 'azure']:
        return jsonify({'error': 'Invalid provider'}), 400
    
    historical_data = fetch_historical_data(provider)
    historical_data.rename(columns={'date': 'ds', 'amount_usd': 'y'}, inplace=True)
    
    forecast = create_forecast(historical_data)
    forecast['amount_usd'] = forecast['amount_usd'].round(2)
    
    return jsonify(forecast.to_dict(orient='records'))

# Register the blueprint in the main application
def register_routes(app):
    app.register_blueprint(cost_forecast_bp)