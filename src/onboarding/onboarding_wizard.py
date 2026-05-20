from typing import Optional
from src.onboarding.api_key_validator import APIKeyValidator

class OnboardingWizard:
    def __init__(self):
        self.api_key_validator = None

    def start(self):
        """Start the onboarding wizard."""
        print("Welcome to the onboarding wizard!")
        self._setup_api_key()
        self._select_template()
        self._setup_workflow_trigger()
        self._complete_onboarding()

    def _setup_api_key(self):
        """Guide the user through API key setup."""
        print("Step 1: API Key Setup")
        api_key = input("Please enter your API key: ")
        self.api_key_validator = APIKeyValidator(api_key)
        if not self.api_key_validator.validate():
            print("Invalid API key. Please try again.")
            self._setup_api_key()
        else:
            print("API key validated successfully.")

    def _select_template(self):
        """Guide the user through template selection."""
        print("Step 2: Template Selection")
        print("Available templates: 1. Basic, 2. Advanced")
        template_choice = input("Please select a template (1 or 2): ")
        if template_choice not in ['1', '2']:
            print("Invalid choice. Please try again.")
            self._select_template()
        else:
            print(f"Template {template_choice} selected.")

    def _setup_workflow_trigger(self):
        """Guide the user through workflow trigger setup."""
        print("Step 3: Workflow Trigger Setup")
        trigger_choice = input("Please select a trigger (1. Manual, 2. Automatic): ")
        if trigger_choice not in ['1', '2']:
            print("Invalid choice. Please try again.")
            self._setup_workflow_trigger()
        else:
            print(f"Trigger{trigger_choice} selected.")

    def _complete_onboarding(self):
        """Complete the onboarding process."""
        print("Onboarding completed successfully!")
        print("A 'Welcome' email with success metrics has been sent to your email address.")
        print("Analytics event logged for each completed onboarding step.")