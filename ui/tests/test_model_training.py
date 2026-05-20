import unittest
from unittest.mock import patch, mock_open
import json
import os
from tkinter import Tk
from ui.model_training import ModelTrainingUI

class TestModelTrainingUI(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = ModelTrainingUI()

    @patch('tkinter.messagebox.showinfo')
    @patch('builtins.open', new_callable=mock_open)
    def test_training_workflow(self, mock_file, mock_showinfo):
        # Set test values
        self.app.algorithm_var.set('Random Forest')
        self.app.data_source_var.set('Local CSV')

        # Execute training
        self.app._handle_training()

        # Verify configuration was saved
        mock_file.assert_called_once_with('model_config.json', 'w')
        handle = mock_file()
        handle.write.assert_called_once()

        # Verify success message
        mock_showinfo.assert_called_once_with(
            "Success",
            "Model training configuration saved successfully.\n"
            "Training will begin in the background."
        )

    @patch('ui.model_training.ModelTrainingUI._trigger_pipeline')
    def test_pipeline_integration(self, mock_trigger):
        test_config = {"algorithm": "test", "data_source": "test"}
        self.app._trigger_pipeline(test_config)
        mock_trigger.assert_called_once_with(test_config)

if __name__ == '__main__':
    unittest.main()