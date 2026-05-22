import unittest
from src.email_template import EmailTemplate

class TestEmailTemplate(unittest.TestCase):
    def setUp(self):
        self.email_template = EmailTemplate()

    def test_render(self):
        user_name = "John Doe"
        total_balance = 1000.00
        mom_change = 5.0
        rendered_template = self.email_template.render(user_name, total_balance, mom_change)
        self.assertIn(user_name, rendered_template)
        self.assertIn(str(total_balance), rendered_template)
        self.assertIn(str(mom_change), rendered_template)

if __name__ == '__main__':
    unittest.main()