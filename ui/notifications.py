import logging
from datetime import datetime

class NotificationSystem:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def send_alert(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = f"[ALERT] {timestamp}: {message}"
        self.logger.warning(alert_message)

    def send_notification(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notification_message = f"[NOTIFICATION] {timestamp}: {message}"
        self.logger.info(notification_message)

def main():
    notifier = NotificationSystem()
    notifier.send_alert("Critical issue detected in validation process.")
    notifier.send_notification("Validation process completed successfully.")

if __name__ == "__main__":
    main()