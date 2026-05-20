from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Any

from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    current_app,
)
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# ------------------------------------------------------------------
# Helper – build the data structure that the template expects
# ------------------------------------------------------------------
def _build_user_credits(user) -> Dict[str, Any]:
    """
    Return a dict with the credit information that the template uses.
    Replace the attribute names with whatever your User model exposes.
    """
    return {
        "monthly": {
            "balance": user.monthly_credits,
            "total": user.monthly_credits_total,
            "reset_date": user.monthly_reset_date,
        },
        "bulk": {
            "balance": user.bulk_credits,
            "total": user.bulk_credits_total,
            "reset_date": user.bulk_reset_date,
        },
    }


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@dashboard_bp.route("/credits")
@login_required
def credits() -> str:
    """
    Render the credit dashboard page.
    """
    credits = _build_user_credits(current_user)
    return render_template("dashboard/credits.html", credits=credits)


@dashboard_bp.route("/credits/data")
@login_required
def credits_data() -> Any:
    """
    Return JSON data for the usage chart.
    The data is generated on the fly; replace with a DB query if you
    store usage history.
    """
    # Example: last 30 days of usage
    today = datetime.utcnow().date()
    dates = [(today - timedelta(days=i)).isoformat() for i in reversed(range(30))]
    # Random data – replace with real usage numbers
    usage = [int(30 + 20 * (i % 5) + (i % 3) * 5) for i in range(30)]

    return jsonify(
        {
            "labels": dates,
            "data": usage,
        }
    )