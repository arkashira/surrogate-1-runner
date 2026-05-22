from abc import ABC, abstractmethod
from typing import Dict, List

class CloudProvider(ABC):
    @abstractmethod
    def parse(self, data: Dict) -> List[Dict]:
        pass

class AWS(CloudProvider):
    def parse(self, data: Dict) -> List[Dict]:
        # ... (AWS parsing logic from Candidate 2)
        pass

class GCP(CloudProvider):
    def parse(self, data: Dict) -> List[Dict]:
        # ... (GCP parsing logic from Candidate 2)
        pass

class Azure(CloudProvider):
    def parse(self, data: Dict) -> List[Dict]:
        # ... (Azure parsing logic from Candidate 2)
        pass