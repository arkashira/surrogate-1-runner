import time
from typing import Dict, Set
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize the rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
        self.locked_users: Set[str] = set()
    
    def is_allowed(self, user_id: str) -> bool:
        """
        Check if a user is allowed to make a request.
        
        Args:
            user_id: Identifier for the user
            
        Returns:
            True if the request is allowed, False otherwise
        """
        current_time = time.time()
        
        # Remove old requests outside the window
        while self.requests[user_id] and self.requests[user_id][0] <= current_time - self.window_seconds:
            self.requests[user_id].popleft()
        
        # Check if user is locked out
        if user_id in self.locked_users:
            return False
        
        # Allow request if under limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(current_time)
            return True
        
        # Lock user out if they exceed the limit
        self.locked_users.add(user_id)
        return False
    
    def unlock_user(self, user_id: str):
        """
        Unlock a user manually.
        
        Args:
            user_id: Identifier for the user
        """
        self.locked_users.discard(user_id)
    
    def reset_user(self, user_id: str):
        """
        Reset a user's request history.
        
        Args:
            user_id: Identifier for the user
        """
        self.requests[user_id].clear()
        self.locked_users.discard(user_id)
    
    def get_remaining_requests(self, user_id: str) -> int:
        """
        Get the number of remaining requests for a user.
        
        Args:
            user_id: Identifier for the user
            
        Returns:
            Number of remaining requests
        """
        current_time = time.time()
        
        # Remove old requests outside the window
        while self.requests[user_id] and self.requests[user_id][0] <= current_time - self.window_seconds:
            self.requests[user_id].popleft()
        
        return max(0, self.max_requests - len(self.requests[user_id]))
    
    def cleanup_expired_locks(self):
        """
        Clean up expired locks (in case of long-running processes).
        """
        # This method could be called periodically to clean up stale locks
        pass