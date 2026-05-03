
import json
from datetime import datetime, timedelta

def aggregate_mau():
    today = datetime.now()
    start_of_month = today.replace(day=1)
    
    # Placeholder for reading events from storage
    with open('/opt/axentx/surrogate-1/src/analytics/event_log.jsonl', 'r') as f:
        events = [json.loads(line) for line in f.readlines()]

    active_users_today = set()
    active_users_month = set()

    for event in events:
        event_time = datetime.fromtimestamp(event['timestamp'])
        if event_time.date() == today.date():
            active_users_today.add(event['user_id'])
        if event_time >= start_of_month:
            active_users_month.add(event['user_id'])

    # Store or print the counts
    print(f"Active users today: {len(active_users_today)}")
    print(f"Active users this month: {len(active_users_month)}")

# Example usage
# aggregate_mau()