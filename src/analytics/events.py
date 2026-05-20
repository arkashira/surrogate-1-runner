from datetime import datetime
import uuid

class AnalyticsEvent:
    def __init__(self, event_type, data=None):
        self.event_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.event_type = event_type
        self.data = data or {}

    def serialize(self):
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'data': self.data
        }

def record_build_completed_event(build_data):
    event = AnalyticsEvent('build_completed', build_data)
    # Assuming there's a function to send events to an analytics service
    send_analytics_event(event.serialize())

def send_analytics_event(event_data):
    # Placeholder for actual implementation of sending the event
    print(f"Sending analytics event: {event_data}")

# Example usage:
# record_build_completed_event({'components': ['CPU', 'GPU'], 'total_cost': 1500})