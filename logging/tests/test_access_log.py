import unittest
import os
from access_log import AccessLog

class TestAccessLog(unittest.TestCase):
    def setUp(self):
        self.log_file = 'test_access.log'
        self.access_log = AccessLog(self.log_file)

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_log_access(self):
        self.access_log.log_access('test_user', 'shell_access', {'ip': '192.168.1.1'})
        logs = self.access_log.get_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['user'], 'test_user')
        self.assertEqual(logs[0]['action'], 'shell_access')

    def test_get_logs(self):
        self.access_log.log_access('test_user1', 'shell_access', {'ip': '192.168.1.1'})
        self.access_log.log_access('test_user2', 'shell_access', {'ip': '192.168.1.2'})
        logs = self.access_log.get_logs()
        self.assertEqual(len(logs), 2)

if __name__ == '__main__':
    unittest.main()