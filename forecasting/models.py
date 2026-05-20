from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

class ExponentialSmoothingForecaster:
    def __init__(self, trend='add', seasonal='mul', seasonal_periods=30):
        self.model = None
        self.trend = trend
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        
    def fit(self, time_series):
        """Train the forecasting model on historical time series data"""
        self.model = ExponentialSmoothing(
            time_series,
            trend=self.trend,
            seasonal=self.seasonal,
            seasonal_periods=self.seasonal_periods
        ).fit()
        
    def predict(self, steps):
        """Generate forecast for specified number of future steps"""
        return self.model.forecast(steps).tolist()