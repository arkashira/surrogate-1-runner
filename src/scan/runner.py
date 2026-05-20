import os
import yaml

def load_compliance_config():
    config_path = os.path.join(os.path.dirname(__file__), '../../.surrogate/compliance.yml')
    if not os.path.exists(config_path):
        return {'enabled': False}
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config or {'enabled': False}

def should_run_scan():
    config = load_compliance_config()
    return config.get('enabled', False)

def run_scan():
    if not should_run_scan():
        print("Compliance scan is disabled.")
        return
    
    # Add the logic to execute the compliance scan here
    print("Running compliance scan...")

if __name__ == "__main__":
    run_scan()