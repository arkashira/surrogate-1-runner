
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Alert:
    """
    Representation of an alert event.

    Attributes
    ----------
    alert_id : str
        Unique identifier for the alert type (e.g., metric name).
    fired_at : datetime.datetime
        Timestamp when the alert fired.
    incident_created : bool
        Whether an incident has been created for this alert firing.
    """
    alert_id: str
    fired_at: datetime.datetime
    incident_created: bool = False

class NoiseDetector:
    """
    Detects and manages noise alerts based on firing frequency.

    Parameters
    ----------
    threshold : int, default 10
        Number of firings within the window required to classify as noise.
    window : datetime.timedelta, default 24 hours
        Sliding time window for counting firings.
    """

    def __init__(self, threshold: int = 10, window: datetime.timedelta | None = None):
        self.threshold = threshold
        self.window = window or datetime.timedelta(hours=24)
        self._noise_alerts: Set[str] = set()
        self._overridden: Set[str] = set()

    def _current_time(self) -> datetime.datetime:
        """Hook for current time; can be overridden in tests."""
        return datetime.datetime.now(datetime.timezone.utc)

    def detect_and_mark(self, alerts: Iterable[Alert]) -> List[Alert]:
        """
        Detects noise alerts in the provided list and updates internal state.

        Parameters
        ----------
        alerts : Iterable[Alert]
            Collection of alert events to analyze.

        Returns
        -------
        List[Alert]
            The same list of alerts; the method updates internal noise state.
        """
        now = self._current_time()
        window_start = now - self.window

        # Group alerts by alert_id within the window
        counts: Dict[str, int] = {}
        incident_map: Dict[str, bool] = {}

        for alert in alerts:
            if alert.fired_at < window_start:
                continue  # Outside the 24h window
            counts[alert.alert_id] = counts.get(alert.alert_id, 0) + 1
            # If any incident exists for this alert_id, mark it
            if alert.incident_created:
                incident_map[alert.alert_id] = True

        # Determine noise alerts
        for alert_id, count in counts.items():
            if count > self.threshold and not incident_map.get(alert_id, False):
                self._noise_alerts.add(alert_id)

        return list(alerts)

    def is_noise(self, alert_id: str) -> bool:
        """
        Checks whether an alert_id is currently classified as noise.

        Parameters
        ----------
        alert_id : str
            The alert identifier to check.

        Returns
        -------
        bool
            True if the alert is noise and not overridden.
        """
        return alert_id in self._noise_alerts and alert_id not in self._overridden

    def override(self, alert_id: str) -> None:
        """
        User overrides the noise classification for a specific alert.

        Parameters
        ----------
        alert_id : str
            The alert identifier to override.
        """
        self._overridden.add(alert_id)

    def remove_override(self, alert_id: str) -> None:
        """
        Removes a user override, restoring the original noise classification.

        Parameters
        ----------
        alert_id : str
            The alert identifier to remove override for.
        """
        self._overridden.discard(alert_id)

    def get_visible_alerts(self, alerts: Iterable[Alert]) -> List[Alert]:
        """
        Returns alerts that should be visible in the default view.

        Alerts classified as noise and not overridden are hidden.

        Parameters
        ----------
        alerts : Iterable[Alert]
            Collection of alert events to filter.

        Returns
        -------
        List[Alert]
            Alerts that are visible.
        """
        visible = []
        for alert in alerts:
            if self.is_noise(alert.alert_id):
                continue  # Hide noise alerts
            visible.append(alert)
        return visible

# /opt/axentx/surrogate-1/services/alert_service.py

class AlertService:
    # ... other methods ...

    def __init__(self, noise_detector):
        self.noise_detector = noise_detector

    def get_alerts(self, is_noise=False, override=None):
        alerts = self.alert_data.copy()
        if is_noise:
            alerts = self.noise_detector.get_visible_alerts(alerts)

        if override is not None:
            alerts.loc[alerts['alert_id'] == override, 'is_noise'] = not alerts.loc[alerts['alert_id'] == override, 'is_noise'].values[0]

        return alerts

# /opt/axentx/surrogate-1/templates/alerts.html

<!-- ... other HTML ... -->

<div class="alert-list">
  {% for alert in alerts %}
    <div class="alert {{ alert.is_noise ? 'noise' : '' }}">
      <span class="alert-id">{{ alert.alert_id }}</span>
      <span class="alert-message">{{ alert.message }}</span>
      {% if alert.is_noise %}
        <button class="override-button" onclick="overrideAlert('{{ alert.alert_id }}')">Override</button>
      {% endif %}
    </div>
  {% endfor %}
</div>

<!-- ... other HTML ... -->