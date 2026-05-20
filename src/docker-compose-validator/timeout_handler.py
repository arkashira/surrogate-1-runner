import logging
import subprocess
import time
import sys

class TimeoutHandler:
    def __init__(self, container_name, max_timeout=30):
        self.container_name = container_name
        self.max_timeout = max_timeout
        self.logger = logging.getLogger(__name__)

    def check_health(self):
        try:
            # Check the container logs for health check status
            logs = subprocess.check_output(
                ["docker", "logs", self.container_name],
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            if "PostgreSQL failed to bind port 5432" in logs:
                self.logger.error("PostgreSQL failed to bind port 5432")
                return False
            if "healthy" in logs:
                self.logger.info("PostgreSQL is healthy")
                return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error checking logs: {e.output.decode('utf-8')}")
            return False
        return None

    def validate_compose(self):
        start_time = time.time()
        while time.time() - start_time < self.max_timeout:
            health_status = self.check_health()
            if health_status is False:
                self.logger.error("PostgreSQL health check failed")
                return False
            elif health_status is True:
                return True
            time.sleep(1)
        self.logger.error("PostgreSQL health check timed out")
        return False

    def exit_compose(self, status):
        # Exit Docker Compose with non-zero status if health check fails
        print(f"Exiting Docker Compose with status {status}")
        sys.exit(status)

# Example usage:
if __name__ == "__main__":
    container_name = "your_postgres_container_name"  # Replace with your actual container name
    timeout_handler = TimeoutHandler(container_name)
    if not timeout_handler.validate_compose():
        timeout_handler.exit_compose(1)