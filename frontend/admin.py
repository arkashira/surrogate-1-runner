"""
Admin blueprint for managing user roles.

Features:
- List users and their roles
- Add a role to a user
- Remove a role from a user
- Modify a user's role
- Audit logging of all role changes
- Role-based access control (only users with 'admin' role can access)

Assumptions:
- Flask app uses Flask-Login for user session management.
- SQLAlchemy is configured and available as `db`.
- User, Role, and AuditLog models exist or are defined below.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Import the SQLAlchemy instance and models
from . import db
from .models import User, Role, UserRole, AuditLog

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(fn):
    """Decorator to ensure the current user has the 'admin' role."""
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.has_role('admin'):
            abort(403)
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def log_action(action, target_user, performed_by):
    """Create an audit log entry."""
    entry = AuditLog(
        action=action,
        target_user_id=target_user.id,
        performed_by_id=performed_by.id,
        timestamp=datetime.utcnow()
    )
    db.session.add(entry)
    db.session.commit()

@admin_bp.route('/users')
@admin_required
def list_users():
    """Display all users with their roles."""
    users = User.query.all()
    return render_template('admin/list_users.html', users=users)

@admin_bp.route('/users/<int:user_id>/add_role', methods=['GET', 'POST'])
@admin_required
def add_role(user_id):
    """Add a role to a user."""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        role_name = request.form.get('role')
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            flash(f"Role '{role_name}' does not exist.", 'danger')
            return redirect(url_for('admin.add_role', user_id=user_id))
        if user.has_role(role_name):
            flash(f"User already has role '{role_name}'.", 'warning')
            return redirect(url_for('admin.list_users'))
        try:
            user.roles.append(role)
            db.session.commit()
            log_action(f"added role '{role_name}'", user, current_user)
            flash(f"Role '{role_name}' added to {user.username}.", 'success')
        except IntegrityError:
            db.session.rollback()
            flash("Failed to add role due to a database error.", 'danger')
        return redirect(url_for('admin.list_users'))
    roles = Role.query.all()
    return render_template('admin/add_role.html', user=user, roles=roles)

@admin_bp.route('/users/<int:user_id>/remove_role', methods=['POST'])
@admin_required
def remove_role(user_id):
    """Remove a role from a user."""
    user = User.query.get_or_404(user_id)
    role_name = request.form.get('role')
    role = Role.query.filter_by(name=role_name).first()
    if not role or not user.has_role(role_name):
        flash(f"User does not have role '{role_name}'.", 'warning')
        return redirect(url_for('admin.list_users'))
    try:
        user.roles.remove(role)
        db.session.commit()
        log_action(f"removed role '{role_name}'", user, current_user)
        flash(f"Role '{role_name}' removed from {user.username}.", 'success')
    except Exception:
        db.session.rollback()
        flash("Failed to remove role due to a database error.", 'danger')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/users/<int:user_id>/modify_role', methods=['GET', 'POST'])
@admin_required
def modify_role(user_id):
    """Modify a user's role (replace old role with new)."""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        old_role_name = request.form.get('old_role')
        new_role_name = request.form.get('new_role')
        old_role = Role.query.filter_by(name=old_role_name).first()
        new_role = Role.query.filter_by(name=new_role_name).first()
        if not old_role or not new_role:
            flash("Specified roles do not exist.", 'danger')
            return redirect(url_for('admin.modify_role', user_id=user_id))
        if not user.has_role(old_role_name):
            flash(f"User does not have role '{old_role_name}'.", 'warning')
            return redirect(url_for('admin.list_users'))
        try:
            user.roles.remove(old_role)
            user.roles.append(new_role)
            db.session.commit()
            log_action(f"modified role from '{old_role_name}' to '{new_role_name}'", user, current_user)
            flash(f"Role changed from '{old_role_name}' to '{new_role_name}' for {user.username}.", 'success')
        except Exception:
            db.session.rollback()
            flash("Failed to modify role due to a database error.", 'danger')
        return redirect(url_for('admin.list_users'))
    roles = Role.query.all()
    return render_template('admin/modify_role.html', user=user, roles=roles)

# Register the blueprint in the main application
# (Assuming the main app imports this module and calls `app.register_blueprint(admin_bp)`)