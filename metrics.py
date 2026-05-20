import time
from collections import defaultdict
from typing import Dict, List, Tuple
import json
import os

class MetricsCollector:
    def __init__(self, storage_path: str = "/tmp/axentx_metrics.json"):
        self.storage_path = storage_path
        self.metrics = defaultdict(list)
        self._load_existing_metrics()
    
    def record_access(self, model_id: str, duration_seconds: float):
        """Record a model access event with duration"""
        timestamp = time.time()
        self.metrics[model_id].append({
            'timestamp': timestamp,
            'duration': duration_seconds
        })
        self._save_metrics()
    
    def get_access_frequency(self, model_id: str, time_window_hours: int = 24) -> int:
        """Get number of accesses in the specified time window"""
        now = time.time()
        window_start = now - (time_window_hours * 3600)
        
        count = 0
        for entry in self.metrics[model_id]:
            if entry['timestamp'] >= window_start:
                count += 1
        return count
    
    def get_total_duration(self, model_id: str, time_window_hours: int = 24) -> float:
        """Get total duration of accesses in the specified time window"""
        now = time.time()
        window_start = now - (time_window_hours * 3600)
        
        total_duration = 0.0
        for entry in self.metrics[model_id]:
            if entry['timestamp'] >= window_start:
                total_duration += entry['duration']
        return total_duration
    
    def get_all_metrics(self) -> Dict[str, List[Dict]]:
        """Get all recorded metrics"""
        return dict(self.metrics)
    
    def _load_existing_metrics(self):
        """Load existing metrics from storage"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    loaded_data = json.load(f)
                    # Convert string keys back to original format
                    for key, value in loaded_data.items():
                        self.metrics[key] = value
            except Exception:
                # If loading fails, start fresh
                pass
    
    def _save_metrics(self):
        """Save metrics to persistent storage"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(dict(self.metrics), f)
        except Exception:
            # Silently fail to avoid breaking main functionality
            pass

# Global instance for easy access
metrics_collector = MetricsCollector()

def record_model_access(model_id: str, duration_seconds: float):
    """Record a model access event"""
    metrics_collector.record_access(model_id, duration_seconds)

def get_model_access_frequency(model_id: str, time_window_hours: int = 24) -> int:
    """Get access frequency for a model"""
    return metrics_collector.get_access_frequency(model_id, time_window_hours)

def get_model_total_duration(model_id: str, time_window_hours: int = 24) -> float:
    """Get total access duration for a model"""
    return metrics_collector.get_total_duration(model_id, time_window_hours)

def get_all_model_metrics() -> Dict[str, List[Dict]]:
    """Get all model metrics"""
    return metrics_collector.get_all_metrics()