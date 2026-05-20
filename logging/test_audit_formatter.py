import unittest
import logging
from audit_formatter import SecurityAuditFormatter

class TestAuditFormatter(unittest.TestCase):
    def test_formatter_output(self):
        record = logging.LogRecord(
            name='security',
            level=logging.WARNING,
            pathname=__file__,
            lineno=0,
            msg='test',
            args=None,
            exc_info=None
        )
        
        record.vulnerability_type = 'SQLi'
        record.request_id = 'req-12345'
        record.request_method = 'POST'
        record.request_path = '/api/data'
        record.user_agent = 'Mozilla/5.0'
        record.client_ip = '192.168.1.1'
        
        formatter = SecurityAuditFormatter()
        formatted = formatter.format(record)
        
        self.assertIn('VULNERABILITY_DETECTED', formatted)
        self.assertIn('request_id=req-12345', formatted)
        self.assertIn('pattern=SQLi', formatted)
        self.assertIn('client_ip=192.168.1.1', formatted)

if __name__ == '__main__':
    unittest.main()