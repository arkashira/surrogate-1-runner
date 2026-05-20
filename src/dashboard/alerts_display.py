from dataclasses import dataclass
from typing import List, Dict
import datetime
from flask import Blueprint, render_template

@dataclass
class Alert:
    """Represents a single budget alert."""
    model: str
    endpoint: str
    usage: float
    budget: float
    timestamp: datetime.datetime
    message: str = ""

class AlertStore:
    """In-memory store for alerts with database persistence option."""
    def __init__(self, use_db: bool = False):
        self._alerts: List[Alert] = []
        self.use_db = use_db
        if use_db:
            from src.models import db, Alert as DBAlert
            self.db = db
            self.DBAlert = DBAlert

    def add(self, alert: Alert) -> None:
        """Add a new alert to the store."""
        self._alerts.append(alert)
        if self.use_db:
            db_alert = self.DBAlert(
                model=alert.model,
                endpoint=alert.endpoint,
                usage=alert.usage,
                budget=alert.budget,
                timestamp=alert.timestamp,
                message=alert.message
            )
            self.db.session.add(db_alert)
            self.db.session.commit()

    def all(self) -> List[Alert]:
        """Return all stored alerts."""
        if self.use_db:
            db_alerts = self.DBAlert.query.all()
            return [Alert(
                model=a.model,
                endpoint=a.endpoint,
                usage=a.usage,
                budget=a.budget,
                timestamp=a.timestamp,
                message=a.message
            ) for a in db_alerts]
        return list(self._alerts)

    def clear(self) -> None:
        """Clear all alerts."""
        self._alerts.clear()
        if self.use_db:
            self.DBAlert.query.delete()
            self.db.session.commit()

def render_alerts(alerts: List[Alert]) -> List[str]:
    """Render a list of alerts into human-readable strings."""
    return [
        f"[{a.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {a.model} ({a.endpoint}) "
        f"usage {a.usage:.2f} exceeded budget {a.budget:.2f}"
        for a in alerts
    ]

# Flask Blueprint for dashboard display
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/alerts')
def display_alerts():
    """Display all alerts in the dashboard."""
    alerts = alert_store.all()
    return render_template('alerts.html', alerts=alerts)

# Initialize store (configure with use_db=True for database persistence)
alert_store = AlertStore(use_db=False)