import yaml
import sys
import os

def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)

def validate_config(config):
    required_keys = ['test_mapping', 'coverage_threshold', 'slack']
    if not all(key in config for key in required_keys):
        print("Invalid config: missing required keys")
        sys.exit(1)
    if not isinstance(config['coverage_threshold'], int):
        print("Invalid config: coverage_threshold must be an integer")
        sys.exit(1)
    if not isinstance(config['slack'], dict) or 'enabled' not in config['slack']:
        print("Invalid config: slack must be a dictionary with 'enabled' key")
        sys.exit(1)

def override_config_with_flags(config, flags):
    if '--no-coverage' in flags:
        config['coverage_threshold'] = 0
    if '--threshold' in flags:
        threshold_index = flags.index('--threshold')
        if threshold_index + 1 < len(flags):
            config['coverage_threshold'] = int(flags[threshold_index + 1])
        else:
            print("Invalid flags: --threshold requires a value")
            sys.exit(1)
    return config

def load_and_validate_config(config_file, flags):
    config = load_config(config_file)
    if config is None:
        # Load default config
        config = {
            'test_mapping': {},
            'coverage_threshold': 80,
            'slack': {'enabled': False}
        }
    config = override_config_with_flags(config, flags)
    validate_config(config)
    return config