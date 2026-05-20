from datetime import datetime, timedelta
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def load_cost_data(provider):
    # Placeholder function to load cost data from different providers
    # This should be replaced with actual data loading logic
    data = {
        'date': pd.date_range(end=datetime.now(), periods=30, freq='D'),
        'cost': [i * 100 + i * 10 for i in range(30)]  # Example cost data
    }
    return pd.DataFrame(data)

def forecast_costs(provider):
    data = load_cost_data(provider)
    model = ARIMA(data['cost'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=30)
    forecast_dates = pd.date_range(start=data['date'].max() + timedelta(days=1), periods=30, freq='D')
    forecast_data = [{'date': date, 'cost': cost} for date, cost in zip(forecast_dates, forecast)]
    return forecast_data

def get_forecast_data():
    providers = ['AWS', 'GCP', 'Azure']
    forecast_data = []
    for provider in providers:
        forecast_data.extend(forecast_costs(provider))
    return forecast_data

if __name__ == "__main__":
    forecast_data = get_forecast_data()
    print(forecast_data)