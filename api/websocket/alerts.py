import asyncio
import websockets
import json
from datetime import datetime

# Simulated data store for alert groups
alert_groups = [
    {
        "title": "High CPU Usage",
        "service": "Service A",
        "alert_count": 5,
        "first_seen": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat(),
        "severity": "critical",
        "member_alerts": [
            {"id": 1, "message": "CPU usage above 90%"},
            {"id": 2, "message": "CPU usage above 85%"},
        ],
    },
    {
        "title": "Disk Space Low",
        "service": "Service B",
        "alert_count": 3,
        "first_seen": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat(),
        "severity": "warning",
        "member_alerts": [
            {"id": 3, "message": "Disk space below 10%"},
        ],
    },
    # Additional alert groups can be added here
]

# Function to sort alert groups
def sort_alert_groups(groups):
    severity_order = {"critical": 1, "warning": 2, "info": 3}
    return sorted(groups, key=lambda x: (severity_order[x["severity"]], -x["alert_count"]))

async def alert_handler(websocket, path):
    while True:
        sorted_groups = sort_alert_groups(alert_groups)
        await websocket.send(json.dumps(sorted_groups))
        await asyncio.sleep(2)  # Simulate real-time updates every 2 seconds

async def main():
    async with websockets.serve(alert_handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())