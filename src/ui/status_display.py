import json
from flask import Blueprint, render_template, request, jsonify
from .database import get_db

bp = Blueprint('status_display', __name__)

@bp.route('/status')
def show_status():
    db = get_db()
    formatting_status = db.execute(
        'SELECT repository, status, last_updated FROM formatting_status'
    ).fetchall()
    return render_template('status_display.html', formatting_status=formatting_status)

@bp.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    repository = data.get('repository')
    status = data.get('status')

    db = get_db()
    db.execute(
        'INSERT OR REPLACE INTO formatting_status (repository, status, last_updated) VALUES (?, ?, datetime("now"))',
        (repository, status)
    )
    db.commit()
    return jsonify({'success': True}), 200