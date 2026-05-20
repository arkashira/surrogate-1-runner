import argparse
import yaml
from flask import Flask, jsonify
import sys

app = Flask(__name__)

class DatadogEmulator:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.validate_config()
        self.app = Flask(__name__)
        
    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def validate_config(self):
        required_fields = ['api_key', 'app_key']
        missing_fields = [field for field in required_fields if field not in self.config]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    def start(self):
        @self.app.route('/api/v1/metrics', methods=['POST'])
        def metrics():
            return jsonify({"status": "success", "message": "Metrics received"})

        self.app.run(port=8080)

def main():
    parser = argparse.ArgumentParser(description="Start the Datadog emulator.")
    parser.add_argument('action', choices=['start', 'stop'], help='Action to perform')
    parser.add_argument('service', choices=['datadog'], help='Service to emulate')
    parser.add_argument('--config', required=True, help='Path to the configuration file')

    args = parser.parse_args()

    if args.action == 'start':
        emulator = DatadogEmulator(args.config)
        emulator.start()
    elif args.action == 'stop':
        # Placeholder for stopping the emulator
        print("Stopping the Datadog emulator")
        sys.exit(0)

if __name__ == "__main__":
    main()