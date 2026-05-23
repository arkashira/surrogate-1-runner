import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DB_PATH = os.environ.get('TRIAL_DB_PATH', '/opt/axentx/surrogate-1/data/trial_subscriptions.db')

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create trials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hardware_id TEXT UNIQUE NOT NULL,
            trial_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            trial_end TIMESTAMP,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create trial_tokens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trial_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trial_id INTEGER,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP,
            FOREIGN KEY (trial_id) REFERENCES trials (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_trial_token(trial_id: int) -> str:
    """Generate a secure trial token for the given trial ID."""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(days=7)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO trial_tokens (trial_id, token, expires_at) VALUES (?, ?, ?)',
        (trial_id, token, expires_at)
    )
    conn.commit()
    conn.close()
    
    return token

@app.route('/api/trial/activate', methods=['POST'])
def activate_trial():
    """Activate a trial subscription with email and hardware ID."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'email' not in data or 'hardware_id' not in data:
            return jsonify({'error': 'Email and hardware ID are required'}), 400
        
        email = data['email'].strip().lower()
        hardware_id = data['hardware_id'].strip()
        
        # Validate email format (basic validation)
        if '@' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
            
        # Validate hardware ID
        if not hardware_id:
            return jsonify({'error': 'Hardware ID cannot be empty'}), 400
        
        # Check if trial already exists
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check existing trial
        cursor.execute(
            'SELECT id, active FROM trials WHERE email = ? OR hardware_id = ?',
            (email, hardware_id)
        )
        existing_trial = cursor.fetchone()
        
        if existing_trial:
            trial_id, is_active = existing_trial
            if is_active:
                # Trial already active
                cursor.execute(
                    'SELECT token FROM trial_tokens WHERE trial_id = ? ORDER BY expires_at DESC LIMIT 1',
                    (trial_id,)
                )
                result = cursor.fetchone()
                if result:
                    return jsonify({
                        'message': 'Trial already activated',
                        'token': result[0],
                        'expires_in_days': 7
                    }), 200
                else:
                    # Generate new token for existing active trial
                    token = generate_trial_token(trial_id)
                    return jsonify({
                        'message': 'Trial already activated',
                        'token': token,
                        'expires_in_days': 7
                    }), 200
            else:
                # Trial expired, reactivate it
                trial_end = datetime.now() + timedelta(days=7)
                cursor.execute(
                    'UPDATE trials SET active = 1, trial_end = ?, trial_start = CURRENT_TIMESTAMP WHERE id = ?',
                    (trial_end, trial_id)
                )
                
                # Generate new token
                token = generate_trial_token(trial_id)
                
                conn.commit()
                conn.close()
                return jsonify({
                    'message': 'Trial reactivated',
                    'token': token,
                    'expires_in_days': 7
                }), 200
        
        # Create new trial
        trial_end = datetime.now() + timedelta(days=7)
        cursor.execute(
            'INSERT INTO trials (email, hardware_id, trial_end) VALUES (?, ?, ?)',
            (email, hardware_id, trial_end)
        )
        trial_id = cursor.lastrowid
        
        # Generate token
        token = generate_trial_token(trial_id)
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Trial activated successfully',
            'token': token,
            'expires_in_days': 7
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)