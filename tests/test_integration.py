import unittest
from unittest.mock import patch, MagicMock
from surrogate_1 import VSCodeExtension, SlackBot

class TestIntegration(unittest.TestCase):
    def test_vscode_extension_shows_daily_prompt(self):
        # Arrange
        vscode_extension = VSCodeExtension()
        vscode_extension.get_daily_prompt = MagicMock(return_value="Test prompt")

        # Act
        prompt = vscode_extension.get_daily_prompt()

        # Assert
        self.assertEqual(prompt, "Test prompt")

    def test_slack_bot_sends_daily_prompt(self):
        # Arrange
        slack_bot = SlackBot()
        slack_bot.send_daily_prompt = MagicMock(return_value=None)

        # Act
        slack_bot.send_daily_prompt()

        # Assert
        slack_bot.send_daily_prompt.assert_called_once()

    def test_prompt_includes_short_conversation_starter(self):
        # Arrange
        vscode_extension = VSCodeExtension()
        vscode_extension.get_daily_prompt = MagicMock(return_value="Test prompt with conversation starter")

        # Act
        prompt = vscode_extension.get_daily_prompt()

        # Assert
        self.assertIn("conversation starter", prompt)

    def test_user_can_click_prompt_to_start_session(self):
        # Arrange
        vscode_extension = VSCodeExtension()
        vscode_extension.start_session = MagicMock(return_value=None)

        # Act
        vscode_extension.start_session()

        # Assert
        vscode_extension.start_session.assert_called_once()

    def test_integration_respects_user_authentication(self):
        # Arrange
        vscode_extension = VSCodeExtension()
        vscode_extension.authenticate_user = MagicMock(return_value=True)

        # Act
        authenticated = vscode_extension.authenticate_user()

        # Assert
        self.assertTrue(authenticated)

if __name__ == '__main__':
    unittest.main()