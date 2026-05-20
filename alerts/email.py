from django.core.mail import send_mail
from django.conf import settings
from .models import Alert

def send_alert_email(alert):
    """
    Sends an email notification for the given alert.
    
    Args:
        alert (Alert): The alert to send an email for.
    """
    subject = 'Alert: Usage Exceeds Budget Constraints'
    message = f'Alert {alert.id}: {alert.message}'
    from_email = settings.EMAIL_HOST_USER
    to_email = settings.EMAIL_RECIPIENT
    send_mail(subject, message, from_email, [to_email])