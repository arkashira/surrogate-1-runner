import requests
import json

class TerraformAPI:
    def __init__(self, workspace_url):
        self.workspace_url = workspace_url
        self.workflow_automator_url = "https://workflow-automator.com/api/v1/workflows"

    def connect_workspace(self):
        response = requests.post(self.workflow_automator_url, json={
            "workspace_url": self.workspace_url,
            "events": ["terraform_plan", "terraform_apply"]
        })
        if response.status_code == 201:
            print("Terraform workspace connected successfully")
            return True
        else:
            print(f"Failed to connect Terraform workspace: {response.text}")
            return False

    def trigger_workflow(self, workflow_name):
        response = requests.post(f"{self.workflow_automator_url}/{workflow_name}/trigger", json={})
        if response.status_code == 200:
            print(f"Workflow {workflow_name} triggered successfully")
            return True
        else:
            print(f"Failed to trigger workflow {workflow_name}: {response.text}")
            return False

    def get_events(self):
        response = requests.get(self.workflow_automator_url + "/events")
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return []

# tests
# src/test_terraform_integration.py
import unittest
from unittest.mock import Mock
from src.terraform_integration import TerraformAPI

class TestTerraformAPI(unittest.TestCase):
    def test_connect_workspace(self):
        terraform_api = TerraformAPI("https://example.com/terraform/workspace")
        self.assertTrue(terraform_api.connect_workspace())

    def test_trigger_workflow(self):
        terraform_api = TerraformAPI("https://example.com/terraform/workspace")
        self.assertTrue(terraform_api.trigger_workflow("my_workflow"))

    def test_get_events(self):
        terraform_api = TerraformAPI("https://example.com/terraform/workspace")
        self.assertIsInstance(terraform_api.get_events(), list)

if __name__ == "__main__":
    unittest.main()

## Summary
- Implemented Terraform API integration with Workflow Automator
- Connected Terraform workspace to Workflow Automator
- Triggered workflows from Terraform
- Retrieved Terraform workspace events
- Added unit tests for Terraform API integration