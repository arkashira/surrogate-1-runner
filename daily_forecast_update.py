import pandas as pd
from datetime import datetime, timedelta
from forecasting.models import ExponentialSmoothingForecaster
from data_ingestion.db import HistoricalUsageDB
from utils.logging import get_logger

logger = get_logger(__name__)

def update_daily_forecasts():
    """Generate updated cost forecasts using historical usage patterns"""
    try:
        # Fetch historical usage data from last 90 days
        db = HistoricalUsageDB()
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)
        
        historical_data = db.query_usage_by_date_range(
            start_date=start_date,
            end_date=end_date
        )
        
        # Convert to time series DataFrame
        ts_data = pd.DataFrame(historical_data)
        ts_data['date'] = pd.to_datetime(ts_data['usage_date'])
        ts_data = ts_data.set_index('date').resample('D').sum()
        
        # Train forecasting model
        model = ExponentialSmoothingForecaster(
            trend='add',
            seasonal='mul',
            seasonal_periods=30
        )
        model.fit(ts_data['cost'])
        
        # Generate 30-day forecast
        forecast_days = 30
        forecast = model.predict(forecast_days)
        forecast_df = pd.DataFrame({
            'forecast_date': [end_date + timedelta(days=i) for i in range(1, forecast_days+1)],
            'predicted_cost': forecast
        })
        
        # Save forecast to database
        db.save_forecast(forecast_df)
        logger.info(f"Successfully updated {forecast_days}-day forecast with {len(forecast_df)} predictions")
        
    except Exception as e:
        logger.error(f"Forecast update failed: {str(e)}")
        raise

if __name__ == "__main__":
    update_daily_forecasts()