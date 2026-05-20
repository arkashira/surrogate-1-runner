class InAppNotification:
    def __init__(self, notification_service):
        self.notification_service = notification_service

    def send_alert(self, user_id, message):
        self.notification_service.notify(user_id, message)

# Example usage
# in_app_notification = InAppNotification(notification_service)
# in_app_notification.send_alert('user123', 'An unusual pattern has been detected in your cloud costs.')