# Alert thresholds in USD
ALERT_THRESHOLDS = {
    'warning': 10000,
    'critical': 20000
}

# Notification endpoints
NOTIFICATION_ENDPOINTS = {
    'email': 'cloud-alerts@axentx.com',
    'in_app': 'https://api.axentx.com/notifications'
}

# Email configuration
EMAIL_CONFIG = {
    'sender': 'alerts@axentx.com',
    'password': 'secure_password_here',
    'smtp_server': 'smtp.axentx.com',
    'port': 465
}