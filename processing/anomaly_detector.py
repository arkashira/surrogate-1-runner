import pandas as pd
import numpy as np
from scipy.stats import norm
import yaml
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

class AnomalyDetector:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.alert_threshold = self.config['alert_threshold']
        self.email_config = self.config['email']

    def calculate_rolling_average(self, data):
        return data.rolling(window=3).mean()

    def detect_anomalies(self, data):
        rolling_avg = self.calculate_rolling_average(data)
        deviations = np.abs((data - rolling_avg) / rolling_avg)
        anomalies = data[deviations > self.alert_threshold]
        return anomalies

    def send_alert(self, message):
        msg = MIMEText(message)
        msg['Subject'] = 'Expense Anomaly Detected'
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.email_config['from'], self.email_config['password'])
            server.sendmail(self.email_config['from'], self.email_config['to'], msg.as_string())

    def process_expenses(self, expenses_data):
        anomalies = self.detect_anomalies(expenses_data)
        if not anomalies.empty:
            alert_message = f"Anomalies detected:\n{anomalies}"
            self.send_alert(alert_message)

def main():
    config_path = '/opt/axentx/surrogate-1/config/alert_rules.yaml'
    detector = AnomalyDetector(config_path)
    
    # Example data loading, replace with actual data source
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    expenses_data = pd.Series(np.random.rand(len(date_range)) * 1000, index=date_range)
    
    detector.process_expenses(expenses_data)

if __name__ == "__main__":
    main()