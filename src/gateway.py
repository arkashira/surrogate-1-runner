import logging
from security import SecurityManager

class Gateway:
    def __init__(self):
        self.security_manager = SecurityManager()
        logging.basicConfig(level=logging.INFO)

    def connect_to_ai_model(self, model_name):
        if not self.security_manager.is_access_granted():
            logging.error("Access denied: VPN or privileged account required.")
            return False
        
        # Simulate connection to AI model
        logging.info(f"Connecting to AI model: {model_name}")
        # Connection logic here...
        logging.info("Successfully connected to the AI model.")
        return True

if __name__ == "__main__":
    gateway = Gateway()
    gateway.connect_to_ai_model("example_model")