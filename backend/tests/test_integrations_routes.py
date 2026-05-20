import unittest
from backend.routes.integrations_routes import test_cloudwatch_connection
from backend.services.cloudwatch_client import CloudWatchClient

class TestIntegrationsRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(integrations_bp)

    def test_test_cloudwatch_connection(self):
        with self.app.test_request_context(json={
            'access_key': 'test_access_key',
            'secret_key': 'test_secret_key'
        }):
            result = test_cloudwatch_connection()
            self.assertIn('success', result.json)
            self.assertIn('message', result.json)

if __name__ == '__main__':
    unittest.main()