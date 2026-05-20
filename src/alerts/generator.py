import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from src.notifications.email import send_email_alert
from src.notifications.in_app import send_in_app_notification
from src.config import ALERT_THRESHOLDS, NOTIFICATION_ENDPOINTS

class AlertGenerator:
    def __init__(self, historical_data_path):
        self.historical_data_path = historical_data_path
        self.model = LinearRegression()
        self.alert_thresholds = ALERT_THRESHOLDS
        self.notification_endpoints = NOTIFICATION_ENDPOINTS

    def load_historical_data(self):
        """Load and preprocess historical cost data"""
        data = pd.read_csv(self.historical_data_path)
        data['time'] = pd.to_datetime(data['time'])
        return data

    def train_model(self, data):
        """Train predictive model on historical data"""
        X = data[['time']].apply(lambda x: x.timestamp()).values.reshape(-1, 1)
        y = data['cost'].values
        self.model.fit(X, y)

    def predict_cost(self, future_time):
        """Predict future cost using trained model"""
        future_timestamp = pd.to_datetime(future_time).timestamp()
        return self.model.predict([[future_timestamp]])[0]

    def check_thresholds(self, predicted_cost):
        """Check if predicted cost exceeds any thresholds"""
        alerts = []
        for threshold_name, threshold_value in self.alert_thresholds.items():
            if predicted_cost > threshold_value:
                alerts.append({
                    'threshold': threshold_name,
                    'value': threshold_value,
                    'predicted_cost': predicted_cost
                })
        return alerts

    def generate_alert(self, current_time, future_time):
        """Generate and send alerts for predicted costs"""
        historical_data = self.load_historical_data()
        self.train_model(historical_data)
        predicted_cost = self.predict_cost(future_time)
        alerts = self.check_thresholds(predicted_cost)

        if alerts:
            alert_message = f"Cost Alert: Predicted cost at {future_time}: ${predicted_cost:.2f}\n"
            alert_message += "Thresholds exceeded:\n"
            for alert in alerts:
                alert_message += f"- {alert['threshold']}: ${alert['value']} (Predicted: ${alert['predicted_cost']:.2f})\n"
            alert_message += "\nRecommended actions:\n1. Review recent resource usage\n2. Optimize underutilized resources\n3. Check for cost anomalies"

            # Send notifications
            send_email_alert(alert_message, self.notification_endpoints['email'])
            send_in_app_notification(alert_message, self.notification_endpoints['in_app'])

            return True
        return False