"""
Compliance deadline tracker that schedules alerts and integrates with calendar apps.
"""

from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Optional

from icalendar import Calendar, Event
from icalendar import vCalAddress, vText

from .user import User
from ..data.compliance_data_processor import Deadline, load_deadlines

class ComplianceTracker:
    """
    Tracks compliance deadlines and schedules alerts.
    """

    def __init__(self, deadlines_csv: Path):
        self.deadlines: List[Deadline] = load_deadlines(deadlines_csv)

    def _compute_alert_date(self, deadline_date: date, days_before: int) -> date:
        """
        Compute the alert date given a deadline date and days_before.
        """
        return deadline_date - timedelta(days=days_before)

    def _create_ical_event(self, deadline: Deadline, alert_date: date, user: User) -> Calendar:
        """
        Create an iCalendar event for the alert.
        """
        cal = Calendar()
        cal.add("prodid", "-//axentx/surrogate-1//Compliance Alerts//EN")
        cal.add("version", "2.0")

        event = Event()
        event.add("summary", f"Compliance Alert: {deadline.name}")
        event.add("dtstart", datetime.combine(alert_date, datetime.min.time()))
        event.add("dtend", datetime.combine(alert_date, datetime.min.time()) + timedelta(hours=1))
        event.add("description", f"{deadline.description}\nDeadline: {deadline.date.isoformat()}")
        event.add("uid", f"{deadline.name}-{alert_date.isoformat()}-{user.user_id}")

        # Attendee
        attendee = vCalAddress(f"MAILTO:{user.email}")
        attendee.params["cn"] = vText(user.email)
        attendee.params["role"] = vText("REQ-PARTICIPANT")
        event.add("attendee", attendee, encode=0)

        cal.add_component(event)
        return cal

    def schedule_alerts_for_user(self, user: User) -> List[Calendar]:
        """
        Schedule alerts for a given user based on their preferences.
        Returns a list of iCalendar objects that can be exported or sent via email.
        """
        if not user.alert_pref.enabled:
            return []

        alerts: List[Calendar] = []
        today = date.today()
        for deadline in self.deadlines:
            alert_date = self._compute_alert_date(deadline.date, user.alert_pref.days_before)
            if alert_date < today:
                # Skip past alerts
                continue
            cal = self._create_ical_event(deadline, alert_date, user)
            alerts.append(cal)
            # For demo purposes, also add to user's in-memory calendar
            user.add_calendar_event({
                "summary": f"Compliance Alert: {deadline.name}",
                "start": alert_date.isoformat(),
                "end": (datetime.combine(alert_date, datetime.min.time()) + timedelta(hours=1)).isoformat(),
                "description": f"{deadline.description}\nDeadline: {deadline.date.isoformat()}",
            })
        return alerts