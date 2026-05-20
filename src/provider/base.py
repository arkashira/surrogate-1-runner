from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models import LLMResponse

class BaseProvider(ABC):
    """Abstract base class for all LLM providers."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text using the provider's API."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider's name."""
        pass