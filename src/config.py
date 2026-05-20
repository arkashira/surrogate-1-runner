import os

def load_config():
    config_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_file, 'r') as f:
        import yaml
        return yaml.safe_load(f)

def get_slack_enabled(config):
    return config.get('slack', {}).get('enabled', False)

def get_github_token():
    return os.environ.get('GITHUB_TOKEN')