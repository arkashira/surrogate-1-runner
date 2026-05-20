import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import IsolationForest

class HistoricalUsageAnalyzer:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = None
        self.model = None

    def load_data(self) -> pd.DataFrame:
        """Load historical usage data from CSV."""
        self.data = pd.read_csv(self.data_path)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        return self.data

    def preprocess_data(self) -> pd.DataFrame:
        """Preprocess data for analysis."""
        if self.data is None:
            self.load_data()

        self.data.set_index('timestamp', inplace=True)
        self.data.sort_index(inplace=True)
        return self.data

    def train_anomaly_detection(self, contamination: float = 0.01) -> IsolationForest:
        """Train an anomaly detection model."""
        self.preprocess_data()
        features = self.data.select_dtypes(include=[np.number]).columns
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.model.fit(self.data[features])
        return self.model

    def predict_anomalies(self) -> pd.DataFrame:
        """Predict anomalies in the data."""
        if self.model is None:
            self.train_anomaly_detection()

        self.preprocess_data()
        features = self.data.select_dtypes(include=[np.number]).columns
        anomalies = self.model.predict(self.data[features])
        self.data['anomaly'] = anomalies
        return self.data[self.data['anomaly'] == -1]

    def forecast_usage(self, steps: int = 7) -> Dict[str, List[float]]:
        """Forecast future usage."""
        self.preprocess_data()
        forecast_results = {}

        for column in self.data.select_dtypes(include=[np.number]).columns:
            model = ARIMA(self.data[column], order=(5,1,0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=steps)
            forecast_results[column] = forecast.tolist()

        return forecast_results

    def analyze_usage_patterns(self) -> Dict[str, Dict]:
        """Analyze historical usage patterns."""
        self.preprocess_data()
        analysis_results = {}

        for column in self.data.select_dtypes(include=[np.number]).columns:
            analysis_results[column] = {
                'mean': self.data[column].mean(),
                'std': self.data[column].std(),
                'trend': self._calculate_trend(column),
                'seasonality': self._calculate_seasonality(column)
            }

        return analysis_results

    def _calculate_trend(self, column: str) -> float:
        """Calculate the trend of a time series."""
        x = np.arange(len(self.data))
        y = self.data[column].values
        slope, _ = np.polyfit(x, y, 1)
        return slope

    def _calculate_seasonality(self, column: str) -> float:
        """Calculate the seasonality of a time series."""
        autocorrelation = self.data[column].autocorr(lag=7)
        return autocorrelation

    def generate_alerts(self, threshold: float = 0.8) -> List[Dict]:
        """Generate predictive cost alerts based on analysis."""
        anomalies = self.predict_anomalies()
        forecast = self.forecast_usage()
        analysis = self.analyze_usage_patterns()

        alerts = []
        for column in analysis:
            trend = analysis[column]['trend']
            seasonality = analysis[column]['seasonality']

            if trend > 0 and seasonality > threshold:
                alert = {
                    'resource': column,
                    'trend': trend,
                    'seasonality': seasonality,
                    'forecast': forecast[column],
                    'recommended_action': self._get_recommended_action(column)
                }
                alerts.append(alert)

        return alerts

    def _get_recommended_action(self, resource: str) -> str:
        """Get recommended action for a resource."""
        actions = {
            'compute': 'Consider scaling down or optimizing compute resources.',
            'storage': 'Review storage usage and consider archiving old data.',
            'network': 'Optimize network usage and consider throttling non-critical traffic.',
            'database': 'Review database queries and consider indexing or caching.'
        }
        return actions.get(resource, 'Review usage patterns and consider optimization strategies.')