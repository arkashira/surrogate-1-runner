import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from src.api.subscription import app

client = TestClient(app)

def test_create_subscription():
    subscription_data = {
        "user_id": "test_user",
        "plan_id": "premium_plan",
        "payment_token": "valid_token"
    }
    response = client.post("/subscriptions", json=subscription_data)
    assert response.status_code == 200
    assert response.json()["user_id"] == "test_user"
    assert response.json()["is_active"] is True

def test_get_user_subscriptions():
    # First, create a subscription
    subscription_data = {
        "user_id": "test_user",
        "plan_id": "premium_plan",
        "payment_token": "valid_token"
    }
    client.post("/subscriptions", json=subscription_data)

    # Then, retrieve the subscription
    response = client.get("/subscriptions/test_user")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == "test_user"