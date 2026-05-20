from flask import Blueprint, jsonify, request, send_file
import csv
import io
from datetime import datetime
from ..services.progress_service import get_user_progress

api_bp = Blueprint('api', __name__)

@api_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Return user's dashboard data including session count, learned terms percentage, and streak."""
    # This would typically fetch from a database or cache
    progress_data = get_user_progress()
    
    return jsonify({
        'total_sessions': progress_data['total_sessions'],
        'terms_learned_percentage': progress_data['terms_learned_percentage'],
        'current_streak': progress_data['current_streak']
    })

@api_bp.route('/export-progress', methods=['GET'])
def export_progress():
    """Export user's progress data as CSV."""
    progress_data = get_user_progress()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'metric',
        'value',
        'timestamp'
    ])
    
    # Write data rows
    writer.writerow([
        'total_sessions',
        progress_data['total_sessions'],
        datetime.now().isoformat()
    ])
    writer.writerow([
        'terms_learned_percentage',
        progress_data['terms_learned_percentage'],
        datetime.now().isoformat()
    ])
    writer.writerow([
        'current_streak',
        progress_data['current_streak'],
        datetime.now().isoformat()
    ])
    
    # Prepare response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='progress_export.csv'
    )