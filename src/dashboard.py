"""
Flask Blueprint that renders a compliance dashboard.

Features
--------
* Real‑time data from a database (pinned actions + full table)
* Query‑string driven filtering, sorting, and pagination
* Graceful fallback to dummy data if the DB is unavailable
* Responsive, accessible HTML template
"""

from flask import Blueprint, render_template, request, current_app
from datetime import datetime
import logging

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _safe_int(val, default=0, min_val=0):
    """Return a safe integer for pagination."""
    try:
        i = int(val)
        return max(i, min_val)
    except (TypeError, ValueError):
        return default


def _build_order_by(sort_column: str, sort_order: str) -> str:
    """Return a safe ORDER BY clause."""
    allowed = {"external_action", "sha", "last_updated"}
    if sort_column not in allowed:
        sort_column = "last_updated"
    sort_order = sort_order.lower()
    if sort_order not in {"asc", "desc"}:
        sort_order = "desc"
    return f"{sort_column} {sort_order}"


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
@dashboard_bp.route("/dashboard")
def show_dashboard():
    """
    Render the compliance dashboard.

    Query parameters
    ----------------
    * filter_column : str  (default: 'external_action')
    * filter_value  : str  (default: '')
    * sort_column   : str  (default: 'last_updated')
    * sort_order    : str  (default: 'desc')
    * page          : int  (default: 1)
    * per_page      : int  (default: 25)
    """
    # Grab query params
    filter_column = request.args.get("filter_column", "external_action")
    filter_value = request.args.get("filter_value", "").strip()
    sort_column = request.args.get("sort_column", "last_updated")
    sort_order = request.args.get("sort_order", "desc")
    page = _safe_int(request.args.get("page"), 1, 1)
    per_page = _safe_int(request.args.get("per_page"), 25, 1)

    # --------------------------------------------------------------------- #
    # 1️⃣  Load pinned actions
    # --------------------------------------------------------------------- #
    pinned_actions = []
    try:
        db = current_app.extensions["db"]  # e.g. Flask‑SQLAlchemy or your own wrapper
        pinned_actions = (
            db.session.query(
                db.compliance_data.c.external_action,
                db.compliance_data.c.sha,
            )
            .filter(db.compliance_data.c.pinned.is_(True))
            .order_by(db.compliance_data.c.last_updated.desc())
            .all()
        )
    except Exception as exc:  # pragma: no cover
        logging.exception("Failed to fetch pinned actions: %s", exc)

    # --------------------------------------------------------------------- #
    # 2️⃣  Build main query
    # --------------------------------------------------------------------- #
    compliance_data = []
    total_rows = 0
    try:
        db = current_app.extensions["db"]
        query = db.session.query(
            db.compliance_data.c.external_action,
            db.compliance_data.c.sha,
            db.compliance_data.c.last_updated,
        )

        # Filtering
        if filter_value:
            column = getattr(db.compliance_data.c, filter_column, None)
            if column is not None:
                query = query.filter(column.ilike(f"%{filter_value}%"))

        # Sorting
        order_by = _build_order_by(sort_column, sort_order)
        query = query.order_by(order_by)

        # Pagination
        total_rows = query.count()
        compliance_data = (
            query.offset((page - 1) * per_page).limit(per_page).all()
        )
    except Exception as exc:  # pragma: no cover
        logging.exception("DB query failed, falling back to dummy data: %s", exc)
        # ----------------------------------------------------------------- #
        # 3️⃣  Dummy data fallback (used when the DB is down)
        # ----------------------------------------------------------------- #
        compliance_data = [
            {
                "external_action": f"Action {i}",
                "sha": f"SHA{i:04d}",
                "last_updated": datetime.utcnow().isoformat() + "Z",
            }
            for i in range(1, 51)
        ]
        total_rows = len(compliance_data)

    # --------------------------------------------------------------------- #
    # 4️⃣  Render template
    # --------------------------------------------------------------------- #
    return render_template(
        "dashboard.html",
        pinned_actions=pinned_actions,
        compliance_data=compliance_data,
        filter_column=filter_column,
        filter_value=filter_value,
        sort_column=sort_column,
        sort_order=sort_order,
        page=page,
        per_page=per_page,
        total_rows=total_rows,
    )