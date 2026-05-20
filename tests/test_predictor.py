
import os
import json
import datetime
import pytest
from pathlib import Path

# Import the predictor module from the surrogate-1 package
try:
    from surrogate_1.predictor import Predictor
except ImportError:
    pytest.skip("Predictor class not found in surrogate_1.predictor", allow_module_level=True)

def generate_synthetic_metrics(days: int = 7):
    """
    Generate synthetic metric data for the past `days` days.
    Each metric dict contains a timestamp and a health value.
    """
    now = datetime.datetime.utcnow()
    metrics = []
    for i in range(days):
        day = now - datetime.timedelta(days=i)
        health = 100 - (i * (30 / days))
        metrics.append({
            "timestamp": day.isoformat() + "Z",
            "health": health
        })
    return metrics

def test_predict_health_accuracy():
    """
    Test that the predictive model runs on synthetic data and
    returns a projected health below 70% when the trend is decreasing.
    """
    predictor = Predictor()
    metrics = generate_synthetic_metrics()

    projected_health = predictor.predict_health(metrics)

    assert projected_health < 70, (
        f"Expected projected health < 70%, got {projected_health:.2f}"
    )
    assert 0.0 <= projected_health <= 100.0, (
        f"Projected health out of bounds: {projected_health}"
    )

def test_predict_health_no_data():
    """
    Test that the predictor handles empty input gracefully.
    """
    predictor = Predictor()
    with pytest.raises(ValueError):
        predictor.predict_health([])

def test_predict_health_invalid_input():
    """
    Test that the predictor raises an error when input data is malformed.
    """
    predictor = Predictor()
    malformed_metrics = [
        {"timestamp": "invalid", "health": "high"},
        {"timestamp": 12345, "health": None}
    ]
    with pytest.raises(TypeError):
        predictor.predict_health(malformed_metrics)

def test_alert():
    """
    Test that the predictor generates the correct alert message when health is below 70%.
    """
    predictor = Predictor()
    predictor.project_health = 65

    alert_message = predictor.alert()

    expected_message = "batteryguard alert\nWarning: Projected health will fall below 70% in 30 days.\nSuggested actions: ...\n"
    assert alert_message == expected_message, "Alert message is incorrect"

if __name__ == '__main__':
    unittest.main()