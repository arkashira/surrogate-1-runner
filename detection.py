"""
Signature drift detection for surrogate-1 pipeline.
Detects when API signatures diverge from expected patterns.
"""
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Detection configuration
DRIFT_THRESHOLD = 0.15  # 15% divergence triggers alert
SIGNATURE_CACHE_DIR = Path("/opt/axentx/surrogate-1/.cache/signatures")
DETECTION_LOG = Path("/opt/axentx/surrogate-1/logs/detections.jsonl")


class SignatureDriftDetector:
    """Detects drift in API signatures across pipeline runs."""
    
    def __init__(self, cache_dir: Path = None, detection_log: Path = None):
        self.cache_dir = cache_dir or SIGNATURE_CACHE_DIR
        self.detection_log = detection_log or DETECTION_LOG
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.detection_log.parent.mkdir(parents=True, exist_ok=True)
        
    def compute_signature(self, request_data: dict) -> str:
        """Compute hash signature for an API request."""
        normalized = json.dumps(request_data, sort_keys=True, default=str)
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    def load_cached_signatures(self, pipeline_name: str) -> dict:
        """Load cached signatures for a pipeline."""
        cache_file = self.cache_dir / f"{pipeline_name}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return {"signatures": {}, "last_updated": None}
    
    def save_cached_signatures(self, pipeline_name: str, data: dict):
        """Save signatures to cache."""
        cache_file = self.cache_dir / f"{pipeline_name}.json"
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def detect_drift(
        self,
        pipeline_name: str,
        request_data: dict,
        affected_api: str = None
    ) -> dict | None:
        """Detect signature drift for a request."""
        current_sig = self.compute_signature(request_data)
        cached = self.load_cached_signatures(pipeline_name)
        
        existing_sigs = cached.get("signatures", {})
        is_new = current_sig not in existing_sigs
        
        if is_new:
            total_sigs = len(existing_sigs)
            drift_score = 1.0 / (total_sigs + 1) if total_sigs > 0 else 1.0
            
            detection = None
            if drift_score >= DRIFT_THRESHOLD:
                detection = {
                    "id": f"drift-{pipeline_name}-{int(time.time())}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "pipeline_name": pipeline_name,
                    "affected_api": affected_api or "unknown",
                    "current_signature": current_sig,
                    "drift_score": drift_score,
                    "total_known_signatures": total_sigs,
                    "status": "detected"
                }
                self._log_detection(detection)
                
                existing_sigs[current_sig] = {
                    "first_seen": datetime.now(timezone.utc).isoformat(),
                    "detection_id": detection.get("id")
                }
                cached["signatures"] = existing_sigs
                self.save_cached_signatures(pipeline_name, cached)
            
            return detection
        
        return None
    
    def _log_detection(self, detection: dict):
        """Append detection to log file."""
        with open(self.detection_log, "a") as f:
            f.write(json.dumps(detection) + "\n")
    
    def get_recent_detections(self, limit: int = 50) -> list:
        """Get recent detections from log."""
        if not self.detection_log.exists():
            return []
        
        detections = []
        with open(self.detection_log) as f:
            for line in f:
                if line.strip():
                    try:
                        detections.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        detections.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return detections[:limit]
    
    def clear_detections(self):
        """Clear detection log."""
        if self.detection_log.exists():
            self.detection_log.unlink()