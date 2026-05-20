from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
import logging
from src.config import config

logger = logging.getLogger(__name__)

email_bp = Blueprint('email', __name__)
mail = Mail()

def init_email_app(app):
    """Initialize mail with Flask app."""
    app.config['MAIL_SERVER'] = config.MAIL_SERVER
    app.config['MAIL_PORT'] = config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
    mail.init_app(app)

@email_bp.route('/send_email', methods=['POST'])
def send_email():
    """
    Send an email to a recipient.
    
    Expected JSON payload:
    {
        "recipient": "email@example.com",
        "subject": "Subject line",
        "body": "Email body text",
        "html": "<p>Optional HTML body</p>"  # optional
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    # Validate required fields
    required_fields = ['recipient', 'subject', 'body']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing': missing_fields
        }), 400
    
    # Validate email format (basic)
    recipient = data['recipient']
    if '@' not in recipient:
        return jsonify({'error': 'Invalid email format'}), 400
    
    try:
        msg = Message(
            subject=data['subject'],
            recipients=[recipient],
            body=data['body'],
            html=data.get('html')
        )
        mail.send(msg)
        
        logger.info(f"Email sent successfully to {recipient}")
        return jsonify({
            'message': 'Email sent successfully',
            'recipient': recipient
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return jsonify({'error': 'Failed to send email', 'details': str(e)}), 500