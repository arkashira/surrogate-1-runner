from .email import EmailService, get_smtp_config

def create_email_service():
    smtp_config = get_smtp_config()
    return EmailService(smtp_config)