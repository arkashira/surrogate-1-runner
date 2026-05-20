import json
import logging

class SecurityConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.settings = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def validate_connection(self):
        # Logic to validate connection without VPN or privileged account
        logging.info("Validating connection for zero-trust gateway.")
        # Placeholder for actual validation logic
        return True

    def log_audit(self, user_id):
        logging.info(f"User {user_id} accessed AI models without VPN or privileged account.")

def main():
    config = SecurityConfig('/opt/axentx/surrogate-1/config/security_config.json')
    if config.validate_connection():
        config.log_audit(user_id='example_user')

if __name__ == "__main__":
    main()