import os
import yaml

def load_default_config():
    """Load the default configuration bundled with the CLI."""
    default_config_path = os.path.join(os.path.dirname(__file__), 'default_config.yaml')
    with open(default_config_path, 'r') as f:
        return yaml.safe_load(f)

def save_config(config, config_path):
    """Save configuration to a YAML file."""
    os.makedirs(os.path.dirname(config_path) if os.path.dirname(config_path) else '.', exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

def validate_config(config):
    """Validate configuration structure and values."""
    required_keys = ['rules']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    
    if not isinstance(config.get('rules', {}), dict):
        raise ValueError("'rules' must be a dictionary")
    
    return True