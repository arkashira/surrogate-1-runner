import os
import json
import logging
from typing import Any, Dict, Optional
import requests

import errors

# Configure a module level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class TerraformConnectionFlow:
    def __init__(self):
        self.workspace_id = os.getenv("TF_WORKSPACE_ID")
        self.automator_url = os.getenv("AUTOMATOR_URL")
        self.automator_token = os.getenv("AUTOMATOR_TOKEN")

    def _get_env_or_raise(self, var_name: str) -> str:
        value = getattr(self, var_name, None)
        if not value:
            raise ValueError(f"Required environment variable '{var_name}' is not set.")
        return value

    def _build_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _handle_error(self, response):
        if response.status_code != 200:
            raise errors.TerraformConnectionError(response.text)
        return response.json()

    def connect_workspace(self, workspace_id=None):
        if workspace_id is None:
            workspace_id = self._get_env_or_raise("TF_WORKSPACE_ID")

        url = f"{self.automator_url.rstrip('/')}/workspaces"
        payload = {"workspace_id": workspace_id}
        headers = self._build_headers(self.automator_token)

        logger.info("Connecting workspace %s to Workflow Automator at %s", workspace_id, url)
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return self._handle_error(response)

    def trigger_workflow(self, workflow_name, payload=None):
        if not self.workspace_id:
            raise ValueError("Terraform workspace ID not set.")
        if not workflow_name:
            raise ValueError("Workflow name must be provided.")

        url = (
            f"{self.automator_url.rstrip('/')}/workspaces/{self.workspace_id}/workflows/{workflow_name}/trigger"
        )
        headers = self._build_headers(self.automator_token)

        logger.info(
            "Triggering workflow '%s' for workspace %s at %s",
            workflow_name,
            self.workspace_id,
            url,
        )
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return self._handle_error(response)

    def log_event(self, event_type, details=None):
        if not self.workspace_id:
            raise ValueError("Terraform workspace ID not set.")

        url = f"{self.automator_url.rstrip('/')}/workspaces/{self.workspace_id}/events"
        payload = {"event_type": event_type, "details": details}
        headers = self._build_headers(self.automator_token)

        logger.info(
            "Logging event '%s' for workspace %s at %s",
            event_type,
            self.workspace_id,
            url,
        )
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return self._handle_error(response)