from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient

# Import the router defined in the service implementation
from src.services.forecast import router


# Assemble a minimal FastAPI app for testing
app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_forecast_endpoint_returns_30_days():
    """The endpoint must return 30 forecast entries with proper fields."""
    response = client.get("/forecast")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 30

    for idx, entry in enumerate(payload):
        # Required keys
        assert "date" in entry
        assert "predicted_cost" in entry
        assert "lower_ci" in entry
        assert "upper_ci" in entry

        # Date should be ISO‑8601 and sequential starting tomorrow
        expected_date = (date.today() + timedelta(days=1 + idx)).isoformat()
        assert entry["date"] == expected_date

        # Numeric values
        assert isinstance(entry["predicted_cost"], (int, float))
        assert isinstance(entry["lower_ci"], (int, float))
        assert isinstance(entry["upper_ci"], (int, float))

        # Confidence interval ordering
        assert entry["lower_ci"] <= entry["predicted_cost"] <= entry["upper_ci"]