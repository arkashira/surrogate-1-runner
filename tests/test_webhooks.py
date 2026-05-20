
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.routes.webhooks import router
from axentx.services.alert_service import AlertService

client = TestClient()
client.include_router(router)

@patch("axentx.services.alert_service.AlertService.send_test_alert")
def test_test_alert(mock_send_test_alert, test_app):
    mock_send_test_alert.return_value = {"success": True}
    response = test_app.post("/test-alert")
    assert response.status_code == 200
    assert response.json() == {"message": "Test alert sent successfully"}