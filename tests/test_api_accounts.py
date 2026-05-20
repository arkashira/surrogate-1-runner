import pytest
from fastapi.testclient import TestClient
from src.api.accounts import router
from src.services.account_manager import AccountManager

client = TestClient(router)

@pytest.fixture
def mock_account_manager(mocker):
    mocker.patch.object(AccountManager, 'create_team_account', return_value=TeamAccount(id='mock-id', name='mock-name', members=['member1']))

def test_create_team_account(mock_account_manager):
    response = client.post("/team_accounts", json={"name": "Test Team", "members": ["user1", "user2"]})
    assert response.status_code == 201
    assert response.json() == {"team_account_id": "mock-id"}