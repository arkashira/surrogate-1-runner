from flask import Flask, render_template, jsonify, request, abort
import os
from datetime import datetime, timezone

app = Flask(__name__, template_folder='templates')

# Configuration
VALID_TOKEN = os.environ.get('DASHBOARD_TOKEN', 'dev-token-12345')
API_ENDPOINT = '/api/violations'

def require_auth(f):
    """Decorator to enforce Bearer token authentication."""
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            abort(401, description='Missing or invalid Authorization header')
        token = auth_header[7:]
        if token != VALID_TOKEN:
            abort(401, description='Invalid token')
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@app.route('/dashboard')
@require_auth
def dashboard():
    """Renders the main dashboard view."""
    token = request.headers.get('Authorization', '')[7:]
    return render_template('dashboard.html', auth_token=token)

@app.route(API_ENDPOINT)
@require_auth
def get_violations():
    """
    Returns violation data structured as:
    {
        "accounts": [
            {
                "account_id": "ACC-0001",
                "total_violations": 10,
                "high_severity_count": 2,
                "last_scan_time": "2023-10-27T10:00:00Z"
            },
            ...
        ]
    }
    """
    accounts = []
    # Generate 200 mock accounts with deterministic data
    now = datetime.now(timezone.utc)
    for i in range(1, 201):
        # Create a realistic decay in violations for later accounts
        total = (i * 7) % 50
        high = max(0, (i * 3) % 15)
        
        # Simulate scan time: newer accounts were scanned more recently
        scan_time = now.timestamp() - (i * 3600) 
        
        accounts.append({
            'account_id': f'ACC-{i:04d}',
            'total_violations': total,
            'high_severity_count': high,
            'last_scan_time': datetime.fromtimestamp(scan_time, timezone.utc).isoformat()
        })
        
    return jsonify({'accounts': accounts})

if __name__ == '__main__':
    app.run(debug=True, port=5000)