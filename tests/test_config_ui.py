import unittest
from unittest.mock import patch
from tkinter import Tk
from src.config_ui import BotConfigUI

class TestBotConfigUI(unittest.TestCase):
    @patch('src.config_ui.print')
    def test_save_config(self, mock_print):
        root = Tk()
        app = BotConfigUI(root)
        
        app.api_key_entry.insert(0, 'test_api_key')
        app.api_secret_entry.insert(0, 'test_secret_key')
        
        app.save_config()
        
        mock_print.assert_called_with("Saving config: API Key=test_api_key, Secret Key=test_secret_key")

    def test_cancel_button(self):
        root = Tk()
        app = BotConfigUI(root)
        
        with patch.object(root, 'destroy') as mock_destroy:
            app.cancel_button.invoke()
            mock_destroy.assert_called_once()

if __name__ == '__main__':
    unittest.main()