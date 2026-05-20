import pytest
from fastapi.testclient import TestClient
from src.api.zero_code_model_training import app

client = TestClient(app)

def test_train_model():
    response = client.post("/train_model", json={"dataset_id": "test_dataset", "model_type": "test_model"})
    assert response.status_code == 200
    assert "training_id" in response.json()

def test_get_model_status():
    response = client.get("/model_status/test_training_id")
    assert response.status_code == 200
    assert "status" in response.json()

def test_get_prebuilt_models():
    response = client.get("/prebuilt_models")
    assert response.status_code == 200
    assert "prebuilt_models" in response.json()