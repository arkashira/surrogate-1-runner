import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class ForecastModel:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.model = LinearRegression()

    def train(self):
        X = np.array(range(len(self.historical_data))).reshape(-1, 1)
        y = np.array(self.historical_data)
        self.model.fit(X, y)

    def predict(self, days):
        X_pred = np.array(range(len(self.historical_data), len(self.historical_data) + days)).reshape(-1, 1)
        return self.model.predict(X_pred)

    def plot_forecast(self, forecast, confidence_intervals=None):
        plt.figure(figsize=(10, 6))
        plt.plot(self.historical_data, label='Historical Data')
        plt.plot(range(len(self.historical_data), len(self.historical_data) + len(forecast)), forecast, label='Forecast')
        if confidence_intervals is not None:
            plt.fill_between(range(len(self.historical_data), len(self.historical_data) + len(forecast)),
                            forecast - confidence_intervals,
                            forecast + confidence_intervals,
                            alpha=0.2, label='Confidence Interval')
        plt.xlabel('Days')
        plt.ylabel('Cost')
        plt.title('Cost Forecast')
        plt.legend()
        plt.show()