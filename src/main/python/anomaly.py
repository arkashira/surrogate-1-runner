"""
Anomaly detection for Surrogate‑1.

* Computes a 30‑day rolling mean and **population** standard deviation.
* Flags a cost as anomalous when it exceeds *threshold_sigma* σ above the mean.
* Returns an alert dictionary; if a SQLAlchemy session is supplied it is persisted.
* Uses a module‑level logger for traceability.
"""

from __future__ import annotations

import datetime
import math
import logging
from typing import Dict, List, Optional, Any

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --------------------------------------------------------------------------- #
# Helper – rolling statistics
# --------------------------------------------------------------------------- #
def _rolling_stats(history: List[float]) -> Optional[Dict[str, float]]:
    """
    Compute mean and population standard deviation for the last 30 days.

    Parameters
    ----------
    history : List[float]
        Daily cost values, most recent last.

    Returns
    -------
    Optional[Dict[str, float]]
        ``{'mean': float, 'std': float}`` or ``None`` if < 30 values.
    """
    if len(history) < 30:
        logger.debug("Insufficient history: %d days – need 30", len(history))
        return None

    recent = history[-30:]
    mean = sum(recent) / 30
    variance = sum((x - mean) ** 2 for x in recent) / 30  # population std
    std = math.sqrt(variance)
    logger.debug("Rolling stats – mean=%.4f, std=%.4f", mean, std)
    return {"mean": mean, "std": std}


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #
def detect_anomaly(
    current_cost: float,
    history: List[float],
    resource_id: str,
    threshold_sigma: float = 3.0,
    *,
    session: Optional[Any] = None,
    alert_model: Optional[Any] = None,
    severity: int = 2,
) -> Optional[Dict[str, Any]]:
    """
    Detect a cost anomaly for a single day.

    Parameters
    ----------
    current_cost : float
        Cost for the day to evaluate.
    history : List[float]
        Historical daily costs (most recent last).  Must contain at least 30
        values for a valid comparison.
    resource_id : str
        Identifier of the monitored resource.
    threshold_sigma : float, optional
        Number of σ above the mean to trigger an anomaly.  Default 3.0.
    session : Optional[Any], optional
        SQLAlchemy session used to persist the alert.  If ``None`` the alert
        is *not* persisted.
    alert_model : Optional[Any], optional
        SQLAlchemy model class that accepts ``timestamp``, ``severity``,
        ``resource`` and ``cost_delta`` as constructor arguments.  Required
        if ``session`` is supplied.
    severity : int, optional
        Severity level to assign to the alert.  Default 2.

    Returns
    -------
    Optional[Dict[str, Any]]
        Alert dictionary if an anomaly is detected, otherwise ``None``.
    """
    stats = _rolling_stats(history)
    if stats is None:
        logger.info("Not enough data to evaluate anomaly for %s", resource_id)
        return None

    mean, std = stats["mean"], stats["std"]
    if std == 0:
        logger.debug("Zero variance – no anomaly possible for %s", resource_id)
        return None

    deviation = current_cost - mean
    sigma = deviation / std
    logger.debug(
        "Resource %s – current=%.4f, mean=%.4f, std=%.4f, sigma=%.4f",
        resource_id,
        current_cost,
        mean,
        std,
        sigma,
    )

    if sigma <= threshold_sigma:
        return None

    # Build the alert payload
    alert = {
        "timestamp": datetime.datetime.utcnow(),
        "severity": severity,
        "resource": resource_id,
        "cost_delta": deviation,
    }

    # Persist if a session and model are supplied
    if session is not None and alert_model is not None:
        try:
            db_alert = alert_model(**alert)
            session.add(db_alert)
            session.commit()
            logger.info("Persisted anomaly alert for %s", resource_id)
        except Exception as exc:  # pragma: no cover
            logger.exception("Failed to persist alert for %s: %s", resource_id, exc)
            # Do not raise – the function still returns the alert dict

    return alert