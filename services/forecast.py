import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import csv
import matplotlib.pyplot as plt

class CloudSpendingForecaster:
    def __init__(self, historical_data):
        self.historical_data = historical_data

    def preprocess_data(self):
        """Preprocess historical data to ensure stationarity."""
        # Convert date column to datetime
        self.historical_data['date'] = pd.to_datetime(self.historical_data['date'])

        # Set date as index
        self.historical_data.set_index('date', inplace=True)

        # Check for stationarity
        result = adfuller(self.historical_data['spending'])
        if result[1] > 0.05:
            # If data is not stationary, apply differencing
            self.historical_data['spending'] = self.historical_data['spending'].diff()
            self.historical_data = self.historical_data.dropna()

    def train_model(self):
        """Train ARIMA model for forecasting."""
        self.preprocess_data()

        # Split data into train and test
        train_size = int(len(self.historical_data) * 0.8)
        train, test = self.historical_data.iloc[:train_size], self.historical_data.iloc[train_size:]

        # Fit ARIMA model
        model = ARIMA(train, order=(5,1,0))
        self.model = model.fit()

        # Forecast
        self.forecast = self.model.get_forecast(steps=90)
        self.confidence_intervals = self.forecast.conf_int()

    def generate_forecast(self):
        """Generate forecast for 30-day and 90-day projections."""
        if not hasattr(self, 'forecast'):
            self.train_model()

        forecast_dates = [self.historical_data.index[-1] + timedelta(days=x) for x in range(1, 91)]
        forecast_values = self.forecast.predicted_mean
        lower_ci = self.confidence_intervals.iloc[:, 0]
        upper_ci = self.confidence_intervals.iloc[:, 1]

        forecast_data = pd.DataFrame({
            'date': forecast_dates,
            'forecast': forecast_values,
            'lower_ci': lower_ci,
            'upper_ci': upper_ci
        })

        return forecast_data

    def plot_forecast(self, forecast_data):
        """Plot forecast as a line chart with confidence interval."""
        plt.figure(figsize=(12, 6))
        plt.plot(self.historical_data.index, self.historical_data['spending'], label='Historical Data')
        plt.plot(forecast_data['date'], forecast_data['forecast'], label='Forecast', color='orange')
        plt.fill_between(forecast_data['date'],
                         forecast_data['lower_ci'],
                         forecast_data['upper_ci'],
                         color='orange', alpha=0.2, label='Confidence Interval')
        plt.title('Cloud Spending Forecast')
        plt.xlabel('Date')
        plt.ylabel('Spending')
        plt.legend()
        plt.grid(True)
        plt.show()

    def export_to_csv(self, forecast_data, filename='cloud_spending_forecast.csv'):
        """Export forecast data to CSV."""
        forecast_data.to_csv(filename, index=False)

# Example usage
if __name__ == "__main__":
    # Load historical data (replace with actual data loading logic)
    historical_data = pd.read_csv('historical_spending.csv')

    # Initialize forecaster
    forecaster = CloudSpendingForecaster(historical_data)

    # Generate forecast
    forecast_data = forecaster.generate_forecast()

    # Plot forecast
    forecaster.plot_forecast(forecast_data)

    # Export to CSV
    forecaster.export_to_csv(forecast_data)