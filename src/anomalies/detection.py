import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AnomalyDetection:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.model = IsolationForest(contamination=0.01)

    def train_model(self):
        self.model.fit(self.data[['usage', 'cost']])

    def detect_anomalies(self):
        self.data['anomaly_score'] = self.model.decision_function(self.data[['usage', 'cost']])
        self.data['anomaly'] = self.model.predict(self.data[['usage', 'cost']])
        anomalies = self.data[self.data['anomaly'] == -1]
        return anomalies

    def send_email_notification(self, anomalies):
        sender_email = "your-email@example.com"
        receiver_email = "receiver-email@example.com"
        password = "your-password"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Anomaly Detected in Budget Usage"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = """\
        Hi,
        Anomalies have been detected in the budget usage.
        Please review the following details:
        {details}
        """.format(details=anomalies.to_string())

        part1 = MIMEText(text, "plain")
        message.attach(part1)

        with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    def run_detection(self):
        self.train_model()
        anomalies = self.detect_anomalies()
        if not anomalies.empty:
            self.send_email_notification(anomalies)
            print("Anomalies detected and notification sent.")
        else:
            print("No anomalies detected.")

# Example usage
if __name__ == "__main__":
    detector = AnomalyDetection("/path/to/budget_data.csv")
    detector.run_detection()