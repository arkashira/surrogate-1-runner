import json
from pathlib import Path

CONFIG_DIR = Path("/opt/axentx/surrogate-1/config")

def get_config(key: str):
    config_path = CONFIG_DIR / f"{key}.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return None

def update_config(key: str, value: dict):
    config_path = CONFIG_DIR / f"{key}.json"
    with open(config_path, "w") as f:
        json.dump(value, f)