import unittest
from user_manager import UserManager
import os

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.test_log_file = 'test_audit.log'
        self.user_manager = UserManager()
        self.user_manager.audit_logger.log_file = self.test_log_file

    def tearDown(self):
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def test_add_user(self):
        self.user_manager.add_user('user123', 'admin')
        with open(self.test_log_file, 'r') as file:
            log_content = file.read()
        self.assertIn('User user123 performed add_user. Details: Role: admin', log_content)

    def test_remove_user(self):
        self.user_manager.remove_user('user123')
        with open(self.test_log_file, 'r') as file:
            log_content = file.read()
        self.assertIn('User user123 performed remove_user. Details: ', log_content)

    def test_modify_user_role(self):
        self.user_manager.modify_user_role('user123', 'editor')
        with open(self.test_log_file, 'r') as file:
            log_content = file.read()
        self.assertIn('User user123 performed modify_user_role. Details: New Role: editor', log_content)

if __name__ == '__main__':
    unittest.main()