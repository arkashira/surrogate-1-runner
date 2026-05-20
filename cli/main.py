import argparse
import os
import yaml
from config import load_default_config, save_config

def parse_args():
    parser = argparse.ArgumentParser(description='Surrogate-1 CLI')
    parser.add_argument('--config', 
                        help='Path to custom config file', 
                        default='config.yaml')
    parser.add_argument('--save-default',
                        help='Save current config as default',
                        action='store_true')
    return parser.parse_args()

def load_config(config_path):
    """Load configuration from specified path or fall back to default."""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    else:
        print(f"Config file '{config_path}' not found. Loading default...")
        return load_default_config()

def main():
    args = parse_args()
    config = load_config(args.config)
    
    if args.save_default:
        default_path = os.path.join(os.path.dirname(__file__), 'default_config.yaml')
        save_config(config, default_path)
        print(f"Config saved as default to {default_path}")
    else:
        print(f"Loaded config from {args.config}")
    
    # Process config (placeholder for actual logic)
    return config

if __name__ == '__main__':
    main()