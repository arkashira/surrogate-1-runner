import re

def sanitize_data(data):
    if not isinstance(data, dict):
        return data

    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            sanitized_data[key] = sanitize_data(value)
        elif isinstance(value, str):
            # Remove any potential PII or sensitive data
            sanitized_data[key] = re.sub(r'\d{3}-\d{2}-\d{4}', '[REDACTED SSN]', value)
            sanitized_data[key] = re.sub(r'\b\d{16}\b', '[REDACTED CREDIT CARD]', sanitized_data[key])
        else:
            sanitized_data[key] = value
    return sanitized_data