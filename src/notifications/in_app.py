from src.integration.notification_service import NotificationService

def send_in_app_notification(message, endpoint):
    """Send in-app notification with cost alert"""
    notification_service = NotificationService(endpoint)
    notification_service.send_notification({
        'type': 'cost_alert',
        'message': message,
        'severity': 'high'
    })