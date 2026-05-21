import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

class AnomalyDetection:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = IsolationForest(contamination=0.01)

    def load_data(self):
        return pd.read_csv(self.data_path)

    def preprocess_data(self, data):
        # Assuming 'cost' is the column we're monitoring for anomalies
        return data[['cost']]

    def train_model(self, preprocessed_data):
        self.model.fit(preprocessed_data)

    def detect_anomalies(self, data):
        preprocessed_data = self.preprocess_data(data)
        predictions = self.model.predict(preprocessed_data)
        anomalies = data[predictions == -1]
        return anomalies

    def send_alert(self, anomalies):
        if not anomalies.empty:
            msg = MIMEText(f"Anomalies detected:\n{anomalies.to_string()}")
            msg['Subject'] = 'Cloud Infrastructure Cost Anomalies Detected'
            msg['From'] = 'cloudoptimize@example.com'
            msg['To'] = 'platform-engineer@example.com'

            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()

def main():
    anomaly_detector = AnomalyDetection('/path/to/cloud_costs.csv')
    data = anomaly_detector.load_data()
    anomaly_detector.train_model(anomaly_detector.preprocess_data(data))
    
    while True:
        current_data = anomaly_detector.load_data()
        anomalies = anomaly_detector.detect_anomalies(current_data)
        anomaly_detector.send_alert(anomalies)
        
        # Check for anomalies every hour
        time.sleep(3600)

if __name__ == "__main__":
    main()