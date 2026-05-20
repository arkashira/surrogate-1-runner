from datetime import datetime, timedelta
from typing import Dict, List
from fastapi import Request

class RateLimiter:
    def __init__(self):
        self.rate_limits: Dict[str, List[datetime]] = {}

    def check_rate_limit(self, user_id: str, action: str, max_requests: int, period: timedelta) -> bool:
        key = f"{user_id}_{action}"
        now = datetime.utcnow()

        # Initialize if not exists
        if key not in self.rate_limits:
            self.rate_limits[key] = []

        # Remove requests older than the period
        self.rate_limits[key] = [request_time for request_time in self.rate_limits[key]
                               if now - request_time <= period]

        # Check if within rate limit
        if len(self.rate_limits[key]) < max_requests:
            self.rate_limits[key].append(now)
            return True
        else:
            return False