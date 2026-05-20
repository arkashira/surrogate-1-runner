from dataclasses import dataclass
from typing import Optional

@dataclass
class ApiConfig:
    """Data model for LLM provider configurations"""
    id: str
    provider: str
    api_key: str
    endpoint: str
    active: bool = True
    description: Optional[str] = None  # Added for better documentation
    created_at: Optional[str] = None   # Added for tracking

    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "provider": self.provider,
            "api_key": self.api_key,
            "endpoint": self.endpoint,
            "active": self.active,
            "description": self.description,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            id=data["id"],
            provider=data["provider"],
            api_key=data["api_key"],
            endpoint=data["endpoint"],
            active=data.get("active", True),
            description=data.get("description"),
            created_at=data.get("created_at")
        )

# /opt/axentx/surrogate-1/api/register.py
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from models.api import ApiConfig

app = Flask(__name__)

# Configuration
STORAGE_FILE = "/opt/axentx/surrogate-1/data/api_configs.json"
SUPPORTED_PROVIDERS = ["openai", "anthropic", "mistral", "custom"]  # Example supported providers

def load_configs():
    """Load API configurations from storage"""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return [ApiConfig.from_dict(item) for item in json.load(f)]
    return []

def save_configs(configs):
    """Save API configurations to storage"""
    with open(STORAGE_FILE, "w") as f:
        json.dump([c.to_dict() for c in configs], f, indent=2)

def validate_provider(provider):
    """Validate provider against supported list"""
    return provider.lower() in SUPPORTED_PROVIDERS or provider.lower() == "custom"

@app.route('/api/register', methods=['POST'])
def register_api():
    """Register or update an LLM provider API configuration"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate required fields
    required_fields = ["provider", "api_key", "endpoint"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate provider
    if not validate_provider(data["provider"]):
        return jsonify({
            "error": f"Unsupported provider: {data['provider']}. Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
        }), 400

    # Generate ID if not provided
    id = data.get("id", f"{data['provider'].lower()}-{data['api_key'][:8]}")

    # Create new config with additional metadata
    new_config = ApiConfig(
        id=id,
        provider=data["provider"].lower(),
        api_key=data["api_key"],
        endpoint=data["endpoint"],
        active=data.get("active", True),
        description=data.get("description"),
        created_at=datetime.now().isoformat()
    )

    # Load existing configs
    configs = load_configs()

    # Update if exists, otherwise add new
    existing = next((c for c in configs if c.id == id), None)
    if existing:
        existing.provider = new_config.provider
        existing.api_key = new_config.api_key
        existing.endpoint = new_config.endpoint
        existing.active = new_config.active
        existing.description = new_config.description
    else:
        configs.append(new_config)

    # Save and return
    save_configs(configs)
    return jsonify(new_config.to_dict()), 201 if not existing else 200

@app.route('/api/configs', methods=['GET'])
def get_configs():
    """Get all registered API configurations"""
    configs = load_configs()
    return jsonify([c.to_dict() for c in configs]), 200

@app.route('/api/configs/<provider>', methods=['GET'])
def get_provider_configs(provider):
    """Get configurations for a specific provider"""
    configs = load_configs()
    provider_configs = [c.to_dict() for c in configs if c.provider == provider.lower()]
    return jsonify(provider_configs), 200

if __name__ == '__main__':
    # Ensure storage directory exists
    os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)