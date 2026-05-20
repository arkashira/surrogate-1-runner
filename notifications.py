"""
Unified notification system for cost‑anomaly detection.

The module is intentionally lightweight so it can be unit‑tested
without external dependencies.  In a real deployment the
`Transport` subclasses would wrap an email/SMS/Slack client.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

# --------------------------------------------------------------------------- #
# Logging configuration – only one handler per module
# --------------------------------------------------------------------------- #
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    _logger.addHandler(handler)


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Anomaly:
    """
    Immutable representation of a detected cost anomaly.

    Attributes
    ----------
    account_id : str
        Cloud account where the anomaly was found.
    metric : str
        Name of the metric that triggered the alert.
    value : float
        Current metric value.
    threshold : float
        Threshold that was exceeded.
    timestamp : str
        ISO‑8601 timestamp of detection.
    """

    account_id: str
    metric: str
    value: float
    threshold: float
    timestamp: str

    def to_dict(self) -> Dict[str, str | float]:
        """Return a JSON‑serialisable representation."""
        return {
            "account_id": self.account_id,
            "metric": self.metric,
            "value": self.value,
            "threshold": self.threshold,
            "timestamp": self.timestamp,
        }


# --------------------------------------------------------------------------- #
# Transport abstraction
# --------------------------------------------------------------------------- #
class Transport:
    """Abstract base for all notification transports."""

    def send(self, user_id: str, message: str) -> None:
        """Send *message* to *user_id*."""
        raise NotImplementedError


class ConsoleTransport(Transport):
    """Fallback transport that prints to stdout – useful for dev & tests."""

    def send(self, user_id: str, message: str) -> None:
        print(f"[Notify] to {user_id}: {message}")


# --------------------------------------------------------------------------- #
# Notification service
# --------------------------------------------------------------------------- #
class NotificationService:
    """
    Orchestrates message creation and delivery.

    Parameters
    ----------
    transport : Transport, optional
        Concrete transport implementation.  Defaults to ``ConsoleTransport``.
    """

    def __init__(self, transport: Optional[Transport] = None) -> None:
        self.transport = transport or ConsoleTransport()

    def send(self, user_id: str, anomaly: Anomaly) -> None:
        """Build and send a notification for *anomaly*."""
        message = self._build_message(anomaly)
        _logger.info("Sending notification to %s: %s", user_id, message)
        self.transport.send(user_id, message)

    @staticmethod
    def _build_message(anomaly: Anomaly) -> str:
        """Human‑readable message – keep it short & clear."""
        return (
            f"⚠️ Cost anomaly detected for account {anomaly.account_id}\n"
            f"Metric: {anomaly.metric}\n"
            f"Value: {anomaly.value} (threshold: {anomaly.threshold})\n"
            f"Time: {anomaly.timestamp}"
        )


# --------------------------------------------------------------------------- #
# Orchestration helper
# --------------------------------------------------------------------------- #
def notify_anomalies(
    anomalies: Iterable[Anomaly],
    user_map: Dict[str, str],
    service: NotificationService,
) -> None:
    """
    Notify users about a batch of anomalies.

    Parameters
    ----------
    anomalies : Iterable[Anomaly]
        Detected anomalies.
    user_map : Dict[str, str]
        Mapping from account_id → user_id.
    service : NotificationService
        Service used to send notifications.
    """
    for anomaly in anomalies:
        user_id = user_map.get(anomaly.account_id)
        if not user_id:
            _logger.warning(
                "No user mapping for account %s; skipping notification",
                anomaly.account_id,
            )
            continue
        service.send(user_id, anomaly)


# --------------------------------------------------------------------------- #
# Example usage – would normally be called by the anomaly detector
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    example = Anomaly(
        account_id="acct-123",
        metric="cpu_hours",
        value=120.5,
        threshold=100.0,
        timestamp="2026-05-14T12:00:00Z",
    )
    mapping = {"acct-123": "user-42"}
    notify_anomalies([example], mapping, NotificationService())