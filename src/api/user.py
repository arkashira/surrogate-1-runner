from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import app
from .models import User, db
from .utils import send_email

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    company_name = data.get('company_name')

    if not email or not password or not company_name:
        return jsonify({'error': 'All fields are required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(email=email, password=generate_password_hash(password), company_name=company_name)
    db.session.add(new_user)
    db.session.commit()

    send_email(email, 'Confirm your email', 'confirm_email', user=new_user)

    return jsonify({'message': 'Registration successful. Please confirm your email.'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Logged in successfully'}), 200