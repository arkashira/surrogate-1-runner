import unittest
from src.security.authentication import Authenticator, AccessController

class TestAuthenticator(unittest.TestCase):
    def test_register_user(self):
        authenticator = Authenticator()
        authenticator.register_user('test_user', 'test_password')
        self.assertIn('test_user', authenticator.users)

    def test_authenticate(self):
        authenticator = Authenticator()
        authenticator.register_user('test_user', 'test_password')
        self.assertTrue(authenticator.authenticate('test_user', 'test_password'))
        self.assertFalse(authenticator.authenticate('test_user', 'wrong_password'))

class TestAccessController(unittest.TestCase):
    def test_grant_permission(self):
        access_controller = AccessController()
        access_controller.grant_permission('test_user', 'read')
        self.assertIn('test_user', access_controller.permissions)
        self.assertIn('read', access_controller.permissions['test_user'])

    def test_revoke_permission(self):
        access_controller = AccessController()
        access_controller.grant_permission('test_user', 'read')
        access_controller.revoke_permission('test_user', 'read')
        self.assertNotIn('read', access_controller.permissions['test_user'])

    def test_has_permission(self):
        access_controller = AccessController()
        access_controller.grant_permission('test_user', 'read')
        self.assertTrue(access_controller.has_permission('test_user', 'read'))
        self.assertFalse(access_controller.has_permission('test_user', 'write'))

if __name__ == '__main__':
    unittest.main()