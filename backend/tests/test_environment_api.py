import unittest
from unittest.mock import patch
from backend.api.environment import api
from backend.models.environment import Environment
from backend.services.aws_service import AWSService

class TestEnvironmentAPI(unittest.TestCase):

    @patch.object(Environment, 'create')
    @patch.object(AWSService, 'create_practice_environment')
    def test_create_environment(self, mock_aws_create, mock_env_create):
        mock_env_create.return_value = Environment(id=1, name="TestEnv")
        response = api.create_environment()
        self.assertEqual(response.status_code, 202)
        self.assertIn("Environment creation initiated", response.json["message"])

    @patch.object(Environment, 'get_by_id')
    def test_get_environment_status(self, mock_get_by_id):
        mock_get_by_id.return_value = Environment(id=1, name="TestEnv", is_ready=True)
        response = api.get_environment_status(1)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Environment is ready for use", response.json["message"])