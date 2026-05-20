import sqlite3
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import datetime, timedelta
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def calculate_forecast_accuracy(data):
    """Calculate MAPE accuracy metric for back-test."""
    # Convert to datetime if needed
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Set timestamp as index and resample to hourly if needed
    data.set_index('timestamp', inplace=True)
    data = data.resample('H').sum()
    
    # Prepare data for forecasting
    series = data['total_cost'].dropna()
    
    if len(series) < 10:  # Need minimum data points
        return float('inf')
    
    # Split data into training and testing sets (last 10% for testing)
    split_point = int(len(series) * 0.9)
    train_data = series[:split_point]
    test_data = series[split_point:]
    
    # Fit Holt-Winters model
    model = ExponentialSmoothing(
        train_data,
        seasonal_periods=24,  # Hourly data, daily seasonality
        trend='add',
        seasonal='add'
    )
    
    fitted_model = model.fit()
    
    # Generate forecast for test period
    forecast = fitted_model.forecast(steps=len(test_data))
    
    # Calculate MAPE
    mape = np.mean(np.abs((test_data.values - forecast.values) / test_data.values)) * 100
    
    return mape

def run_daily_forecast_update():
    """Run the daily forecast update job."""
    try:
        logger.info("Starting daily forecast update...")
        
        # Get data
        data = get_hourly_costs_last_90_days()
        
        # Calculate forecast accuracy
        mape = calculate_forecast_accuracy(data)
        
        logger.info(f"Model accuracy (MAPE): {mape:.2f}%")
        
        # Check if accuracy meets threshold
        if mape <= 15:
            logger.info("Forecast accuracy meets requirements.")
        else:
            logger.warning(f"Forecast accuracy ({mape:.2f}%) exceeds threshold of 15%")
            
        # Calculate and store forecast
        # This would typically involve storing the forecast in the database
        # For now we just log that it ran successfully
        
        logger.info("Daily forecast update completed successfully.")
        
    except Exception as e:
        logger.error(f"Error during daily forecast update: {str(e)}")
        raise

if __name__ == "__main__":
    run_daily_forecast_update()