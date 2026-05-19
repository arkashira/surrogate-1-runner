from flask import Blueprint, render_template
from .dashboard_config import get_connected_repositories

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    """Render dashboard with connected GitHub repositories"""
    repos = get_connected_repositories()
    return render_template('dashboard.html', repositories=repos)