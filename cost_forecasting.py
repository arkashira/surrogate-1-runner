import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import json
import os

class CostForecaster:
    def __init__(self, data_dir='/opt/axentx/surrogate-1/data'):
        self.data_dir = data_dir
        self.historical_data = None
        self.forecast_data = None

    def load_historical_data(self):
        """Load historical usage data from JSON files"""
        files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
        data = []
        for file in files:
            with open(os.path.join(self.data_dir, file), 'r') as f:
                data.append(json.load(f))
        self.historical_data = pd.DataFrame(data)

    def preprocess_data(self):
        """Preprocess the historical data"""
        if self.historical_data is None:
            self.load_historical_data()

        self.historical_data['date'] = pd.to_datetime(self.historical_data['date'])
        self.historical_data.set_index('date', inplace=True)
        self.historical_data.sort_index(inplace=True)

    def generate_forecast(self, days=30):
        """Generate cost forecast using ARIMA model"""
        if self.historical_data is None:
            self.preprocess_data()

        # Simple example using total_cost - in a real implementation, you'd want to forecast per-service
        model = ARIMA(self.historical_data['total_cost'], order=(5,1,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=days)

        forecast_dates = [self.historical_data.index[-1] + timedelta(days=i) for i in range(1, days+1)]
        self.forecast_data = pd.DataFrame({'date': forecast_dates, 'forecasted_cost': forecast})

    def save_forecast(self, output_file='forecast.json'):
        """Save the forecast to a JSON file"""
        if self.forecast_data is None:
            self.generate_forecast()

        self.forecast_data.to_json(output_file, orient='records', date_format='iso')
        print(f"Forecast saved to {output_file}")

    def update_forecast_daily(self):
        """Update the forecast daily"""
        self.load_historical_data()
        self.preprocess_data()
        self.generate_forecast()
        self.save_forecast()

if __name__ == "__main__":
    forecaster = CostForecaster()
    forecaster.update_forecast_daily()