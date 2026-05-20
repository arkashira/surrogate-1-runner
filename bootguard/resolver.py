import subprocess
import logging

# Configure logging for better visibility and debugging.
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class SystemctlWrapper:
    """
    A wrapper class to manage system services using systemctl.
    Provides methods to start, stop, and check the state of services,
    with built-in fallback logic for graceful degradation.
    """
    def __init__(self):
        """
        Initializes the SystemctlWrapper with a logger.
        """
        self.logger = logging.getLogger(__name__)

    def start_service(self, service_name: str) -> bool:
        """
        Starts a system service.

        Args:
            service_name: The name of the service to start.

        Returns:
            True if the service was successfully started, False otherwise.
        """
        return self._manage_service(service_name, 'start')

    def stop_service(self, service_name: str) -> bool:
        """
        Stops a system service.

        Args:
            service_name: The name of the service to stop.

        Returns:
            True if the service was successfully stopped, False otherwise.
        """
        return self._manage_service(service_name, 'stop')

    def _manage_service(self, service_name: str, action: str) -> bool:
        """
        Core method to perform a systemctl action (start/stop).

        Args:
            service_name: The name of the service.
            action: The action to perform ('start' or 'stop').

        Returns:
            True if the action was successful, False otherwise.
        """
        try:
            # Get the service state before the action
            before_state = self._get_service_state(service_name)
            self.logger.info(f"Attempting to {action} {service_name}. Current state: {before_state}")

            # Execute the systemctl command
            subprocess.run(
                ['systemctl', action, service_name],
                check=True,
                capture_output=True,
                text=True
            )

            # Get the service state after the action
            after_state = self._get_service_state(service_name)
            self.logger.info(f"{service_name}: before={before_state}, after={after_state}")

            return True

        except subprocess.CalledProcessError as e:
            # Log the error and trigger fallback
            self.logger.error(f"Failed to {action} {service_name}: {e.stderr}")
            self._fallback(service_name)
            return False

    def _get_service_state(self, service_name: str) -> str:
        """
        Checks the current state of a service.

        Args:
            service_name: The name of the service.

        Returns:
            The state of the service (e.g., 'active', 'inactive').
        """
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to check state of {service_name}: {e.stderr}")
            return "unknown"

    def _fallback(self, service_name: str):
        """
        Implements graceful degradation logic.
        This is a placeholder. Implement specific fallback logic here.
        """
        self.logger.info(f"Falling back for {service_name}. Disabling non-critical service.")
        # Example fallback: stop a non-critical service
        non_critical_service = 'example-non-critical.service'
        self.stop_service(non_critical_service)

# Example usage
if __name__ == "__main__":
    wrapper = SystemctlWrapper()
    
    # Start a service
    wrapper.start_service('example.service')
    
    # Stop a service
    wrapper.stop_service('example.service')