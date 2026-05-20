"""
User model and alert preferences.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

@dataclass
class AlertPreference:
    """
    User's alert preferences.
    """
    days_before: int = 14  # default 14 days before deadline
    enabled: bool = True   # whether alerts are enabled

@dataclass
class User:
    """
    Simple user representation.
    """
    user_id: str
    email: str
    alert_pref: AlertPreference = field(default_factory=AlertPreference)
    calendar_events: List[dict] = field(default_factory=list)  # placeholder for calendar integration

    def add_calendar_event(self, event: dict) -> None:
        """
        Add an event to the user's calendar.
        """
        self.calendar_events.append(event)