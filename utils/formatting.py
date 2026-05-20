import json

def format_status(status_data):
    """Format the status data for CLI output."""
    return json.dumps(status_data, indent=2)