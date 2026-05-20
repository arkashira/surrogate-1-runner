import logging
import subprocess

class TelemetryAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def report_resolution_status(self, service_name, action, success, before_state, after_state):
        if success:
            self.logger.info(f"Successfully {action} service '{service_name}'.")
        else:
            self.logger.warning(f"Failed to {action} service '{service_name}'. Falling back to graceful degradation.")
            self.graceful_degradation(service_name)
        
        self.log_service_state(service_name, before_state, after_state)

    def log_service_state(self, service_name, before_state, after_state):
        self.logger.info(f"Service '{service_name}' state before: {before_state}, after: {after_state}")

    def graceful_degradation(self, service_name):
        # Logic to disable non-critical service
        self.logger.info(f"Disabling non-critical service '{service_name}'.")

    def start_service(self, service_name):
        before_state = self.get_service_state(service_name)
        try:
            subprocess.run(['systemctl', 'start', service_name], check=True)
            after_state = self.get_service_state(service_name)
            self.report_resolution_status(service_name, 'start', True, before_state, after_state)
        except subprocess.CalledProcessError:
            after_state = self.get_service_state(service_name)
            self.report_resolution_status(service_name, 'start', False, before_state, after_state)

    def stop_service(self, service_name):
        before_state = self.get_service_state(service_name)
        try:
            subprocess.run(['systemctl', 'stop', service_name], check=True)
            after_state = self.get_service_state(service_name)
            self.report_resolution_status(service_name, 'stop', True, before_state, after_state)
        except subprocess.CalledProcessError:
            after_state = self.get_service_state(service_name)
            self.report_resolution_status(service_name, 'stop', False, before_state, after_state)

    def get_service_state(self, service_name):
        try:
            result = subprocess.run(['systemctl', 'is-active', service_name], capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            self.logger.error(f"Error getting state for service '{service_name}': {e}")
            return 'unknown'

if __name__ == "__main__":
    agent = TelemetryAgent()
    # Example usage
    agent.start_service('example-service')
    agent.stop_service('example-service')