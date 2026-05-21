import logging
from notifications.alerts import configure_alerts
from notifications.config import Config
from notifications.anomaly import AnomalyDetector

logging.basicConfig(level=logging.INFO)

def main():
    email_config = EmailConfig('your-email@example.com', 'recipient-email@example.com', 'smtp.example.com', 587, 'your-password')
    in_app_config = InAppConfig('https://your-in-app-notification-url.com')
    config = Config(email_config, in_app_config)
    alert_service = configure_alerts(config.email_config, config.in_app_config)

    anomaly_detector = AnomalyDetector(100)
    data = 150
    if anomaly_detector.detect_anomaly(data):
        alert_service.send_email('Anomaly detected', 'Data exceeds threshold')
        alert_service.send_in_app_notification('Anomaly detected', 'Data exceeds threshold')

if __name__ == '__main__':
    main()