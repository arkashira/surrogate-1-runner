import json
import os

def load_config() -> dict:
    """Load configuration from environment or default."""
    config_file = os.getenv("SURROGATE_CONFIG", "config.json")
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "whitelist": [
                "logger", "console", "utils", "math", "datetime",
                "os", "sys", "json", "typing", "collections"
            ]
        }