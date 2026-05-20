from flask import Flask, jsonify
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)

def get_hourly_costs_last_90_days():
    """Fetch hourly cost data for the last 90 days from database."""
    conn = sqlite3.connect('/opt/axentx/surrogate-1/data/costs.db')
    query = """
        SELECT timestamp, total_cost 
        FROM costs 
        WHERE timestamp >= datetime('now', '-90 days')
        ORDER BY timestamp
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def calculate_forecast(data, forecast_days=30):
    """Calculate forecast using Holt-Winters exponential smoothing."""
    # Convert to datetime if needed
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Set timestamp as index and resample to hourly if needed
    data.set_index('timestamp', inplace=True)
    data = data.resample('H').sum()
    
    # Prepare data for forecasting
    series = data['total_cost'].dropna()
    
    if len(series) < 10:  # Need minimum data points
        raise ValueError("Insufficient data for forecasting")
    
    # Fit Holt-Winters model
    model = ExponentialSmoothing(
        series,
        seasonal_periods=24,  # Hourly data, daily seasonality
        trend='add',
        seasonal='add'
    )
    
    fitted_model = model.fit()
    
    # Generate forecast
    forecast = fitted_model.forecast(steps=forecast_days * 24)
    
    # Calculate confidence intervals (95%)
    forecast_ci = fitted_model.get_forecast(steps=forecast_days * 24)
    conf_int = forecast_ci.conf_int()
    
    # Return results
    return {
        'forecast': forecast.tolist(),
        'confidence_interval': {
            'lower': conf_int.iloc[:, 0].tolist(),
            'upper': conf_int.iloc[:, 1].tolist()
        }
    }

@app.route('/api/v1/costs/forecast', methods=['GET'])
def get_cost_forecast():
    try:
        # Get data
        data = get_hourly_costs_last_90_days()
        
        # Calculate forecast
        forecast_result = calculate_forecast(data, 30)
        
        # Calculate total forecasted cost
        total_forecast = sum(forecast_result['forecast'])
        
        # Calculate average confidence interval
        avg_lower = np.mean(forecast_result['confidence_interval']['lower'])
        avg_upper = np.mean(forecast_result['confidence_interval']['upper'])
        
        response = {
            'total': round(total_forecast, 2),
            'confidence_interval': {
                'lower': round(avg_lower, 2),
                'upper': round(avg_upper, 2)
            },
            'forecast_days': 30
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)