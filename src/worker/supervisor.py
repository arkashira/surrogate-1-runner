import datetime
import traceback
from typing import Any, Dict

# ----------------------------------------------------------------------
# Existing imports – kept as comments to preserve original context.
# ----------------------------------------------------------------------
# from .worker import Worker
# from ..config import SETTINGS
# from ..event_bus import EventBus

# ----------------------------------------------------------------------
# Stub implementations for missing project‑specific objects.
# In the real codebase these will be provided by the surrounding modules.
# ----------------------------------------------------------------------
class SETTINGS:
    """Placeholder for project settings."""
    DASHBOARD_URL = "https://dashboard.axentx.com/pipelines"

class EventBus:
    """Very small singleton event bus used for emitting events."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def emit(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Emit an event – real implementation forwards to the messaging layer."""
        # In production this would push to Kafka, PubSub, etc.
        print(f"[EventBus] emitted {event_name}: {payload}")

# ----------------------------------------------------------------------
# Rate‑limiting state (in‑memory).  One entry per pipeline name.
# ----------------------------------------------------------------------
_last_alert_sent: Dict[str, datetime.datetime] = {}
_ALERT_COOLDOWN = datetime.timedelta(hours=1)

def _should_send_alert(pipeline_name: str) -> bool:
    """Return True if an alert may be sent for *pipeline_name* respecting the 1‑hour limit."""
    now = datetime.datetime.utcnow()
    last_sent = _last_alert_sent.get(pipeline_name)
    if last_sent is None or (now - last_sent) >= _ALERT_COOLDOWN:
        _last_alert_sent[pipeline_name] = now
        return True
    return False

# ----------------------------------------------------------------------
# Supervisor – orchestrates workers and emits `job_failed` events.
# ----------------------------------------------------------------------
class Supervisor:
    """
    Coordinates a set of workers for a single ingestion pipeline.

    Parameters
    ----------
    pipeline_name: str
        Human‑readable identifier of the pipeline (used in alerts).
    user_email: str
        Email address of the pipeline owner – used for alert routing.
    user_settings: dict
        User‑specific configuration; must contain ``email_alerts`` (bool) to
        honour the opt‑out toggle from the dashboard.
    """
    def __init__(self, pipeline_name: str, user_email: str, user_settings: Dict[str, Any]):
        self.pipeline_name = pipeline_name
        self.user_email = user_email
        self.user_settings = user_settings
        self._event_bus = EventBus.get_instance()
        # Placeholder for any additional initialisation the original file performed.
        # ...

    def run_worker(self, worker: Any) -> None:
        """
        Execute a worker and emit a ``job_failed`` event on unhandled exceptions.

        The event payload contains:
            - ``pipeline``: name of the pipeline
            - ``error_snippet``: short traceback excerpt
            - ``dashboard_url``: link to the dashboard filtered to this pipeline
            - ``user_email``: recipient address
        """
        try:
            worker.run()
        except Exception as exc:  # pylint: disable=broad-except
            # Capture a concise error snippet (first line of the traceback)
            tb_lines = traceback.format_exception_only(type(exc), exc)
            error_snippet = tb_lines[0].strip() if tb_lines else str(exc)

            # Respect user opt‑out and rate‑limit before emitting.
            if self.user_settings.get("email_alerts", True):
                if _should_send_alert(self.pipeline_name):
                    payload = {
                        "pipeline": self.pipeline_name,
                        "error_snippet": error_snippet,
                        "dashboard_url": f"{SETTINGS.DASHBOARD_URL}?pipeline={self.pipeline_name}",
                        "user_email": self.user_email,
                    }
                    self._event_bus.emit("job_failed", payload)

            # Re‑raise so upstream logic can decide whether to retry, abort, etc.
            raise

    # ------------------------------------------------------------------
    # Additional methods from the original supervisor implementation would
    # follow here unchanged.
    # ------------------------------------------------------------------
    # def start(self):
    #     ...

    # def stop(self):
    #     ...