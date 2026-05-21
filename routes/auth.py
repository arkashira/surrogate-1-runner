from flask import Blueprint, request, jsonify
import secrets
import string
from datetime import datetime, timedelta
from ..models.user import User
from ..database import db
from ..email_service import send_password_reset_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')
    
    # Validate email presence
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Look up user (case-sensitive per standard; normalize if needed)
    user = User.query.filter_by(email=email).first()
    
    # Security: Always return generic success message
    # This prevents email enumeration attacks
    if not user:
        return jsonify({
            'message': 'If an account exists with that email, a reset link has been sent.'
        }), 200
    
    # Generate cryptographically secure reset token
    reset_token = ''.join(
        secrets.choice(string.ascii_letters + string.digits) 
        for _ in range(32)
    )
    
    # Set expiration (1 hour)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Store token and expiration in user record
    user.reset_token = reset_token
    user.reset_token_expires_at = expires_at
    db.session.commit()
    
    # Send reset email with error handling
    try:
        send_password_reset_email(user.email, reset_token)
    except Exception:
        # Log the exception internally; don't expose details to client
        return jsonify({'error': 'Failed to send reset email'}), 500
    
    return jsonify({'message': 'Password reset link has been sent to your email.'}), 200