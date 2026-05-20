import json
from datetime import datetime, timedelta
from threading import Lock

class SSHAuthenticator:
    def __init__(self, config_path='/opt/axentx/surrogate-1/src/config/ssh_config.json'):
        self.config = self._load_config(config_path)
        self.rate_limit_lock = Lock()
        self.rate_limit_cache = {}

    def _load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def authenticate(self, username, public_key):
        if not self._check_rate_limit(username):
            return False

        # Placeholder for public key authentication logic
        return True

    def _check_rate_limit(self, username):
        max_attempts = self.config.get('max_ssh_attempts', 10)
        time_window = timedelta(minutes=self.config.get('rate_limit_window_minutes', 5))

        with self.rate_limit_lock:
            attempts = self.rate_limit_cache.get(username, [])
            current_time = datetime.now()

            # Remove old attempts outside the time window
            attempts = [attempt for attempt in attempts if current_time - attempt <= time_window]

            if len(attempts) >= max_attempts:
                return False

            attempts.append(current_time)
            self.rate_limit_cache[username] = attempts

        return True


# Example usage
if __name__ == "__main__":
    authenticator = SSHAuthenticator()
    print(authenticator.authenticate("user", "public_key"))  # Output depends on rate limit checks