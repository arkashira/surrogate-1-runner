import unittest
from unittest.mock import patch, MagicMock
from services.onboarding_engine import send_onboarding_email

class TestOnboardingEngine(unittest.TestCase):

    @patch('services.onboarding_engine.smtplib.SMTP')
    @patch('services.onboarding_engine.Environment')
    def test_send_onboarding_email(self, mock_env, mock_smtp):
        user = MagicMock()
        user.name = "Test User"
        user.email = "test@example.com"
        
        step = MagicMock()
        step.title = "Step 1"
        step.description = "This is the first step."

        # Mock the template rendering
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Mocked Email Content</html>"
        mock_env.return_value.get_template.return_value = mock_template

        send_onboarding_email(user, step)

        # Assert that the email was sent
        mock_smtp.return_value.__enter__.return_value.send_message.assert_called_once()

        # Assert that the template was rendered with the correct parameters
        mock_template.render.assert_called_once_with(user=user, step=step)

if __name__ == '__main__':
    unittest.main()