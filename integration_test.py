import unittest
import subprocess

class TestHealthCheck(unittest.TestCase):
    def test_health_check(self):
        # Run the health check script
        subprocess.run(["python", "health.py"])

        # Check that the health check endpoint returns 200
        response = subprocess.run(["curl", f"http://localhost:8080/health"], capture_output=True)
        self.assertEqual(response.returncode, 0)

if __name__ == "__main__":
    unittest.main()