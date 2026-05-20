import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from surrogate_1.cli import cli

class TestCLIValidate(unittest.TestCase):

    def test_cli_validate(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compose-validate'])
        self.assertEqual(result.exit_code, 0)

    def test_cli_validate_with_file(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compose-validate', '-f', 'docker-compose.yml'])
        self.assertEqual(result.exit_code, 0)

    def test_cli_validate_with_quiet_flag(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compose-validate', '--quiet'])
        self.assertEqual(result.exit_code, 0)

    @patch('docker.compose')
    def test_cli_validate_with_unhealthy_containers(self, mock_compose):
        mock_compose.return_value.containers.return_value = [
            {'name': 'container1', 'health_status': 'unhealthy'},
            {'name': 'container2', 'health_status': 'healthy'}
        ]
        runner = CliRunner()
        result = runner.invoke(cli, ['compose-validate'])
        self.assertNotEqual(result.exit_code, 0)

    @patch('docker.compose')
    def test_cli_validate_with_timeout(self, mock_compose):
        mock_compose.return_value.containers.return_value = [
            {'name': 'container1', 'health_status': 'starting'}
        ]
        runner = CliRunner()
        result = runner.invoke(cli, ['compose-validate'])
        self.assertNotEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()