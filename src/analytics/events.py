
import time
import json
from datetime import datetime

# Function to log events
def log_event(event_type, user_id):
    timestamp = int(time.time())
    event_data = {
        'event_type': event_type,
        'user_id': user_id,
        'timestamp': timestamp
    }
    # Assuming we have a function to write to a log file or a database
    write_event_to_storage(event_data)

def write_event_to_storage(event_data):
    # Placeholder for actual storage logic (e.g., database or file)
    with open('/opt/axentx/surrogate-1/src/analytics/event_log.jsonl', 'a') as f:
        f.write(json.dumps(event_data) + '\n')

# Example usage
# log_event('upload', 'user123')
# log_event('search', 'user123')
# log_event('open', 'user123')