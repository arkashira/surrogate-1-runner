import unittest
from terminal.session import TerminalSession

class TestTerminalSession(unittest.TestCase):
    def setUp(self):
        self.session = TerminalSession('localhost')

    def test_register_ssh_key(self):
        public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD...'
        self.session.register_ssh_key(public_key)
        self.assertTrue(hasattr(self.session, 'public_key'))

    def test_create_encrypted_tunnel(self):
        self.session.create_encrypted_tunnel()
        self.assertTrue(self.session.client.get_transport() is not None)

    def test_validate_ssh_tunnel(self):
        result = self.session.validate_ssh_tunnel()
        self.assertTrue(result)

    def tearDown(self):
        self.session.close()

if __name__ == '__main__':
    unittest.main()