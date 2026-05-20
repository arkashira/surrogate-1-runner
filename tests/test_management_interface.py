import unittest
from management.interface import MultiplexerManagementInterface

class TestMultiplexerManagementInterface(unittest.TestCase):
    def setUp(self):
        self.interface = MultiplexerManagementInterface()

    def test_deploy_command(self):
        args = ['deploy', '--config', 'test_config.yaml']
        with unittest.mock.patch('argparse._sys.argv', [''] + args):
            with unittest.mock.patch('subprocess.run') as mock_run:
                self.interface.run()
                mock_run.assert_called_with(["echo", "Deployed"])

    def test_manage_command(self):
        args = ['manage', 'start']
        with unittest.mock.patch('argparse._sys.argv', [''] + args):
            with unittest.mock.patch('subprocess.run') as mock_run:
                self.interface.run()
                mock_run.assert_called_with(["echo", "start"])

if __name__ == '__main__':
    unittest.main()