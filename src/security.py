import logging

class SecurityManager:
    def __init__(self):
        self.user_authenticated = True  # Simulate user authentication

    def is_access_granted(self):
        if not self.user_authenticated:
            logging.warning("User is not authenticated.")
            return False
        # Additional checks for zero-trust model can be added here
        logging.info("Access granted.")
        return True