from datetime import datetime
from typing import Optional
from ..models.playbook import Playbook
from ..repositories.playbook_repository import PlaybookRepository
from ..services.dataset_service import DatasetService

class PlaybookService:
    def __init__(self, playbook_repository: PlaybookRepository, dataset_service: DatasetService):
        self.playbook_repository = playbook_repository
        self.dataset_service = dataset_service

    async def generate_playbook(self, user_id: str, on_demand: bool = False):
        if on_demand:
            # Use the latest dataset data for on-demand generation
            dataset_data = self.dataset_service.get_latest_data()
            playbook = Playbook(
                user_id=user_id,
                content=dataset_data,
                generated_at=datetime.utcnow(),
                is_on_demand=True
            )
        else:
            # Weekly scheduled generation logic
            playbook = Playbook(
                user_id=user_id,
                content="Weekly playbook content",
                generated_at=datetime.utcnow(),
                is_on_demand=False
            )

        self.playbook_repository.save(playbook)