import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from ..services.playbook_service import PlaybookService
from ..repositories.playbook_repository import PlaybookRepository
from ..services.dataset_service import DatasetService

@pytest.mark.asyncio
async def test_generate_on_demand_playbook():
    # Setup
    mock_repo = MagicMock(spec=PlaybookRepository)
    mock_dataset = MagicMock(spec=DatasetService)
    mock_dataset.get_latest_data.return_value = "Latest dataset data"

    service = PlaybookService(mock_repo, mock_dataset)
    user_id = "test_user"

    # Execute
    await service.generate_playbook(user_id, on_demand=True)

    # Verify
    mock_dataset.get_latest_data.assert_called_once()
    mock_repo.save.assert_called_once()
    saved_playbook = mock_repo.save.call_args[0][0]
    assert saved_playbook.user_id == user_id
    assert saved_playbook.content == "Latest dataset data"
    assert saved_playbook.is_on_demand is True