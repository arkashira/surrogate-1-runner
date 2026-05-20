import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class GPT4UsageEvent:
    """Represents a single GPT-4 usage event for analytics."""
    event_id: str
    timestamp: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    request_id: str
    user_id: str
    cost_usd: float
    latency_ms: float
    status: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class GPT4Analytics:
    """Analytics tracker for GPT-4 usage through Surrogate-1 gateway."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.event_store: list[GPT4UsageEvent] = []
        self.metrics = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost_usd': 0.0,
            'total_latency_ms': 0.0,
            'requests_by_status': {},
            'requests_by_user': {},
        }
        self._init_logging()

    def _init_logging(self):
        """Initialize logging for audit trail."""
        log_level = self.config.get('log_level', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"{timestamp}{id(self)}".encode()).hexdigest()[:16]

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        return hashlib.sha256(f"{datetime.utcnow().isoformat()}".encode()).hexdigest()[:12]

    def track_usage(self, user_id: str, request_id: str, 
                    prompt_tokens: int, completion_tokens: int,
                    latency_ms: float, status: str,
                    cost_usd: float = 0.0,
                    metadata: Optional[Dict[str, Any]] = None) -> GPT4UsageEvent:
        """Track a GPT-4 usage event."""
        total_tokens = prompt_tokens + completion_tokens
        event = GPT4UsageEvent(
            event_id=self._generate_event_id(),
            timestamp=datetime.utcnow().isoformat(),
            model="gpt-4",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            request_id=request_id,
            user_id=user_id,
            cost_usd=cost_usd,
            latency_ms=latency_ms,
            status=status,
            metadata=metadata or {}
        )
        
        self.event_store.append(event)
        self._update_metrics(event)
        
        logger.info(f"GPT-4 Usage Event: {event.event_id} | "
                   f"User: {user_id} | Tokens: {total_tokens} | "
                   f"Cost: ${cost_usd:.4f} | Status: {status}")
        
        return event

    def _update_metrics(self, event: GPT4UsageEvent):
        """Update running metrics from event."""
        self.metrics['total_requests'] += 1
        self.metrics['total_tokens'] += event.total_tokens
        self.metrics['total_cost_usd'] += event.cost_usd
        self.metrics['total_latency_ms'] += event.latency_ms
        
        status_key = f"{event.status}_{event.model}"
        self.metrics['requests_by_status'][status_key] = \
            self.metrics['requests_by_status'].get(status_key, 0) + 1
        
        user_key = f"user_{event.user_id}"
        self.metrics['requests_by_user'][user_key] = \
            self.metrics['requests_by_user'].get(user_key, 0) + 1

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary for reporting."""
        return {
            'total_requests': self.metrics['total_requests'],
            'total_tokens': self.metrics['total_tokens'],
            'total_cost_usd': round(self.metrics['total_cost_usd'], 4),
            'average_latency_ms': round(
                self.metrics['total_latency_ms'] / 
                max(self.metrics['total_requests'], 1), 2
            ),
            'requests_by_status': self.metrics['requests_by_status'],
            'requests_by_user': self.metrics['requests_by_user'],
            'event_count': len(self.event_store),
            'generated_at': datetime.utcnow().isoformat()
        }

    def export_events(self) -> list[Dict[str, Any]]:
        """Export all tracked events for audit."""
        return [event.to_dict() for event in self.event_store]

    def clear_events(self):
        """Clear event store (for testing)."""
        self.event_store.clear()
        logger.info("Event store cleared")

    def get_events_for_user(self, user_id: str) -> list[GPT4UsageEvent]:
        """Get all events for a specific user."""
        return [e for e in self.event_store if e.user_id == user_id]