import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import json

class AlertThrottle:
    """
    Alert throttling cache implementation for ingestion job failures.
    """
    
    def __init__(self, cache_backend=None):
        """
        Initialize the alert throttling system.
        
        Args:
            cache_backend: Optional cache backend (default: in-memory)
        """
        self.cache = cache_backend or {}
        self._cache_key_prefix = "alert_throttle:"
    
    def _get_pipeline_key(self, pipeline_name: str) -> str:
        """Get the cache key for a specific pipeline."""
        return f"{self._cache_key_prefix}{pipeline_name}"
    
    def can_send_alert(self, pipeline_name: str) -> bool:
        """
        Check if an alert can be sent for a given pipeline.
        
        Returns:
            True if an alert can be sent (within rate limit), False otherwise
        """
        key = self._get_pipeline_key(pipeline_name)
        
        # Check if we have a record for this pipeline
        if key not in self.cache:
            # Initialize with current time if no record exists
            self.cache[key] = {
                "last_alert": datetime.now().timestamp(),
                "count": 0
            }
            return True
        
        current_time = datetime.now().timestamp()
        last_alert = self.cache[key]["last_alert"]
        
        # Check if it's been more than 1 hour since last alert
        if current_time - last_alert >= 3600:
            # Reset the timer and allow sending
            self.cache[key]["last_alert"] = current_time
            self.cache[key]["count"] = 0
            return True
        
        # Check if we've already sent alerts this hour
        if self.cache[key]["count"] >= 1:
            return False
        
        # Allow sending this hour
        self.cache[key]["count"] += 1
        return True
    
    def record_alert(self, pipeline_name: str):
        """Record that an alert has been sent for this pipeline."""
        key = self._get_pipeline_key(pipeline_name)
        
        if key not in self.cache:
            self.cache[key] = {
                "last_alert": datetime.now().timestamp(),
                "count": 0
            }
        else:
            self.cache[key]["last_alert"] = datetime.now().timestamp()
            self.cache[key]["count"] += 1
    
    def clear_pipeline(self, pipeline_name: str):
        """Clear all throttling records for a specific pipeline."""
        key = self._get_pipeline_key(pipeline_name)
        if key in self.cache:
            del self.cache[key]
    
    def get_status(self, pipeline_name: str) -> Optional[Dict]:
        """Get the current throttling status for a pipeline."""
        key = self._get_pipeline_key(pipeline_name)
        return self.cache.get(key, None)
    
    def get_all_status(self) -> Dict:
        """Get status for all pipelines."""
        return self.cache.copy()