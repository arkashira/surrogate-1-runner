from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/locks')
def locks_dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('locks_dashboard.html')