import asyncio
import json
import logging
from typing import Dict, Set, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class TerminalChange:
    """Represents a change made in the terminal session"""
    user_id: str
    timestamp: datetime
    operation: str  # 'input', 'output', 'cursor_move'
    payload: Dict[str, Any]

class ChangePropagationManager:
    """Manages real-time change propagation among terminal session participants"""
    
    def __init__(self):
        self.participants: Set[str] = set()
        self.change_queue = asyncio.Queue()
        self.subscribers: Dict[str, asyncio.Queue] = {}
        
    def add_participant(self, user_id: str) -> None:
        """Add a participant to the session"""
        self.participants.add(user_id)
        self.subscribers[user_id] = asyncio.Queue()
        logger.info(f"Added participant {user_id} to session")
        
    def remove_participant(self, user_id: str) -> None:
        """Remove a participant from the session"""
        if user_id in self.participants:
            self.participants.remove(user_id)
            if user_id in self.subscribers:
                del self.subscribers[user_id]
            logger.info(f"Removed participant {user_id} from session")
            
    def broadcast_change(self, change: TerminalChange) -> None:
        """Broadcast a change to all participants"""
        # Add to queue for processing
        asyncio.create_task(self._queue_change(change))
        
    async def _queue_change(self, change: TerminalChange) -> None:
        """Queue the change for distribution to subscribers"""
        try:
            # Broadcast to all subscribers
            for user_id, queue in self.subscribers.items():
                await queue.put(change)
        except Exception as e:
            logger.error(f"Failed to broadcast change: {e}")
            
    async def get_changes_for_user(self, user_id: str) -> TerminalChange:
        """Get next change for a specific user"""
        if user_id not in self.subscribers:
            raise ValueError(f"User {user_id} is not subscribed")
        return await self.subscribers[user_id].get()
        
    def get_active_participants(self) -> Set[str]:
        """Get current active participants"""
        return self.participants.copy()

# Global instance
change_manager = ChangePropagationManager()