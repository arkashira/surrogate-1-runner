import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import threading
from collections import deque
import os


@dataclass
class ApiRequestLog:
    timestamp: str
    user_id: str
    endpoint: str
    method: str
    request_data: Dict
    response_data: Dict
    signature: str
    status_code: int


class LogStorage:
    def __init__(self, max_logs: int = 10000):
        self.max_logs = max_logs
        self.logs: deque = deque(maxlen=max_logs)
        self._lock = threading.Lock()
        
    def add_log(self, log_entry: ApiRequestLog):
        """Add a new log entry"""
        with self._lock:
            self.logs.append(log_entry)
    
    def get_logs(self, user_id: Optional[str] = None, 
                 limit: Optional[int] = None) -> List[ApiRequestLog]:
        """Get logs, optionally filtered by user_id"""
        with self._lock:
            logs_list = list(self.logs)
            
            if user_id:
                logs_list = [log for log in logs_list if log.user_id == user_id]
                
            if limit:
                logs_list = logs_list[-limit:]
                
            return logs_list
    
    def search_logs(self, query: str, user_id: Optional[str] = None) -> List[ApiRequestLog]:
        """Search logs by query string"""
        with self._lock:
            logs_list = list(self.logs)
            
            if user_id:
                logs_list = [log for log in logs_list if log.user_id == user_id]
                
            # Simple text search across relevant fields
            results = []
            for log in logs_list:
                log_dict = asdict(log)
                log_str = json.dumps(log_dict, default=str)
                if query.lower() in log_str.lower():
                    results.append(log)
                    
            return results
    
    def export_logs(self, filename: str):
        """Export all logs to JSON file"""
        with self._lock:
            logs_list = list(self.logs)
            with open(filename, 'w') as f:
                json.dump([asdict(log) for log in logs_list], f, indent=2, default=str)
    
    def clear_logs(self):
        """Clear all logs"""
        with self._lock:
            self.logs.clear()
    
    def get_log_count(self) -> int:
        """Get current number of logs"""
        with self._lock:
            return len(self.logs)


# Configuration management
class Config:
    # Logging configuration
    LOG_STORAGE_MAX_LOGS: int = int(os.getenv('LOG_STORAGE_MAX_LOGS', '10000'))
    
    # Database configuration (if using persistent storage)
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    
    # Redis configuration (for real-time updates)
    REDIS_URL: Optional[str] = os.getenv('REDIS_URL')
    
    # File-based logging
    LOG_FILE_PATH: str = os.getenv('LOG_FILE_PATH', '/var/log/surrogate-1/api-logs.json')
    
    @classmethod
    def validate(cls):
        """Validate configuration settings"""
        if cls.LOG_STORAGE_MAX_LOGS <= 0:
            raise ValueError("LOG_STORAGE_MAX_LOGS must be positive")


# Global instance
log_storage = LogStorage(Config.LOG_STORAGE_MAX_LOGS)