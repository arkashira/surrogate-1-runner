
from typing import Dict, Any

# Define the JSON schema for training pairs
TRAINING_PAIR_SCHEMA = {
    "type": "object",
    "properties": {
        "input": {"type": "string"},
        "output": {"type": "string"},
        "label": {"type": "string"},
        "metadata": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "source": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"},
                "id": {"type": "string"}
            },
            "required": ["source", "timestamp", "id"]
        }
    },
    "required": ["input", "output", "label", "metadata"],
    "additionalProperties": False
}