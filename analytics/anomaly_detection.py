import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.ensemble import IsolationForest

class CostAnomalyDetector:
    def __init__(self, window_size=30, threshold=3.0):
        self.window_size = window_size
        self.threshold = threshold
        self.model = IsolationForest(contamination=0.01)

    def load_data(self, file_path):
        """Load historical cost data from CSV file."""
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df

    def preprocess_data(self, df):
        """Preprocess the data by resampling and handling missing values."""
        df = df.resample('D').sum()
        df = df.fillna(method='ffill')
        return df

    def detect_anomalies(self, df):
        """Detect anomalies in the cost data."""
        # Decompose the time series to remove trend and seasonality
        decomposition = seasonal_decompose(df['cost'], model='additive', period=30)
        residual = decomposition.resid

        # Fit the isolation forest model
        self.model.fit(residual.values.reshape(-1, 1))

        # Predict anomalies
        anomalies = self.model.predict(residual.values.reshape(-1, 1))
        anomaly_indices = np.where(anomalies == -1)[0]

        return anomaly_indices

    def get_anomaly_dates(self, df, anomaly_indices):
        """Get the dates of the anomalies."""
        return df.index[anomaly_indices]

    def run(self, file_path):
        """Run the anomaly detection pipeline."""
        df = self.load_data(file_path)
        df = self.preprocess_data(df)
        anomaly_indices = self.detect_anomalies(df)
        anomaly_dates = self.get_anomaly_dates(df, anomaly_indices)
        return anomaly_dates