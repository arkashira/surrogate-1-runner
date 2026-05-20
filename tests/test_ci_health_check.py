import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os

class TestCIHealthCheck(unittest.TestCase):
    @patch('subprocess.run')
    def test_health_check_success(self, mock_run):
        # Mock successful docker compose up
        mock_run.side_effect = [
            subprocess.CompletedProcess(args='', returncode=0),
            subprocess.CompletedProcess(args='', returncode=0, stdout="healthy_container1 healthy_container2")
        ]

        # Test the health check function
        result = self.run_health_check()
        self.assertTrue(result)
        self.assertEqual(mock_run.call_count, 2)

    @patch('subprocess.run')
    def test_health_check_failure(self, mock_run):
        # Mock successful docker compose up
        mock_run.side_effect = [
            subprocess.CompletedProcess(args='', returncode=0),
            subprocess.CompletedProcess(args='', returncode=0, stdout="unhealthy_container1 healthy_container2")
        ]

        # Test the health check function
        with self.assertRaises(SystemExit) as cm:
            self.run_health_check()
        self.assertEqual(cm.exception.code, 1)

    @patch('subprocess.run')
    def test_health_check_disabled(self, mock_run):
        # Set the disable secret
        os.environ['COMPOSE_GUARD_DISABLED'] = 'true'

        # Test the health check function
        result = self.run_health_check()
        self.assertTrue(result)
        self.assertEqual(mock_run.call_count, 0)

    def run_health_check(self):
        # This would be the actual function that runs the health check
        # For testing purposes, we'll simulate its behavior
        try:
            if os.getenv('COMPOSE_GUARD_DISABLED') == 'true':
                return True

            # Simulate running docker compose up
            subprocess.run(['docker', 'compose', 'up', '-d'], check=True)

            # Simulate running the health-wait script
            result = subprocess.run(['./health_wait.sh'], capture_output=True, text=True, check=True)

            # Check if any containers are unhealthy
            unhealthy_containers = [c for c in result.stdout.split() if c != 'healthy']
            if unhealthy_containers:
                print(f"Unhealthy containers: {unhealthy_containers}")
                raise SystemExit(1)

            return True
        except subprocess.CalledProcessError:
            return False

if __name__ == '__main__':
    unittest.main()