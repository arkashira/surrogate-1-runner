from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import re
import psycopg2
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

auth_bp = Blueprint('auth', __name__)

# Email configuration (in production, these should come from env vars)
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USER = 'noreply@axentx.com'
EMAIL_PASS = 'your_email_password'

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    # At least 8 characters, one uppercase, one lowercase, one digit
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

def send_verification_email(email, user_id):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = "Verify Your Email Address"

        body = f"""
        Hello,

        Please verify your email address by clicking the link below:
        http://localhost:5000/verify/{user_id}

        This link will expire in 5 minutes.

        Best regards,
        The Axentx Team
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data['email'].strip()
    password = data['password']
    
    # Validate email format
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate password strength
    if not validate_password(password):
        return jsonify({
            'error': 'Password must be at least 8 characters long and contain uppercase, lowercase, and digit'
        }), 400
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="axentx_db",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        
        # Insert user into database
        cur.execute(
            "INSERT INTO users (email, password_hash, created_at) VALUES (%s, %s, %s) RETURNING id",
            (email, hashed_password, datetime.utcnow())
        )
        user_id = cur.fetchone()[0]
        
        # Create empty profile
        cur.execute(
            "INSERT INTO founder_profiles (user_id, stage, target_market, pricing_model, current_funnel, biggest_growth_pain) VALUES (%s, NULL, NULL, NULL, NULL, NULL)",
            (user_id,)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Send verification email
        if send_verification_email(email, user_id):
            return jsonify({
                'message': 'Account created successfully. Please check your email for verification.',
                'user_id': user_id
            }), 201
        else:
            return jsonify({
                'message': 'Account created but failed to send verification email.',
                'user_id': user_id
            }), 201
            
    except psycopg2.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500