from abc import ABC, abstractmethod
from .model import Alert


class AlertChannel(ABC):
    @abstractmethod
    def send(self, alert: Alert) -> bool:
        """Return True on success, False otherwise."""
        raise NotImplementedError