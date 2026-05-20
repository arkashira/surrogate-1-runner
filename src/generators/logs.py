
import datetime
import random
import string
from typing import Dict, List, Union

def _generate_timestamp() -> str:
    """Generate a realistic Datadog log timestamp (ISO8601 with microseconds)."""
    now = datetime.datetime.now(datetime.timezone.utc)
    return now.isoformat(timespec='microseconds') + 'Z'

def _generate_random_string(length: int = 10) -> str:
    """Generate a random string for log fields."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_log_entry(
    service_name: str,
    log_template: str,
    dimensions: Dict[str, Union[str, int]],
    randomize_fields: bool = True
) -> Dict[str, str]:
    """
    Generate a single synthetic Datadog log entry.

    Args:
        service_name: The name of the service generating the log.
        log_template: A string template with placeholders like {field_name}.
        dimensions: Dictionary of dimension values to inject into the log.
        randomize_fields: If True, add random values to dimensions.

    Returns:
        A dictionary representing the log entry with fields and timestamp.
    """
    entry = dimensions.copy()
    
    entry['timestamp'] = _generate_timestamp()
    entry['service'] = service_name
    
    # Process the log template
    for key, value in entry.items():
        if isinstance(value, str):
            if '{' in log_template and '}' in log_template:
                log_template = log_template.replace(f'{{{key}}}', value)
            else:
                log_template += f'
{key}: {value}'
    
    entry['message'] = log_template
    
    if randomize_fields:
        random_key = _generate_random_string(8)
        random_value = _generate_random_string(12)
        entry[f'random_{random_key}'] = random_value
    
    return entry

def generate_multiple_logs(
    count: int,
    service_name: str,
    log_template: str,
    dimensions: Dict[str, Union[str, int]],
    randomize_fields: bool = True
) -> List[Dict[str, str]]:
    """
    Generate a list of synthetic Datadog log entries.

    Args:
        count: Number of log entries to generate.
        service_name: The name of the service generating the logs.
        log_template: A string template for the log message.
        dimensions: Dictionary of dimension values to use.
        randomize_fields: If True, add random fields to each entry.

    Returns:
        A list of log entry dictionaries.
    """
    logs = []
    for _ in range(count):
        logs.append(generate_log_entry(service_name, log_template, dimensions, randomize_fields))
    return logs

if __name__ == "__main__":
    example_template = "User {user_id} performed action {action} at {timestamp}"
    example_dims = {
        "user_id": "user_123",
        "action": "login",
        "status": "success"
    }
    sample_logs = generate_multiple_logs(3, "auth-service", example_template, example_dims)
    for log in sample_logs:
        print(log)