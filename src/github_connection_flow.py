import logging
import os
from typing import List, Dict, Any, Optional

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class GitHubConnectionError(Exception):
    """Raised when a GitHub API call fails."""


class GitHubConnection:
    """
    Handles the connection between a GitHub repository and the Workflow Automator.

    Typical usage::

        conn = GitHubConnection(token=os.getenv("GITHUB_TOKEN"))
        conn.connect(repo="owner/repo")
        conn.register_webhook(
            webhook_url="https://example.com/webhook",
            events=["push", "pull_request"]
        )
    """

    GITHUB_API_URL = "https://api.github.com"

    def __init__(self, token: str):
        if not token:
            raise ValueError("GitHub token must be provided")
        self.token = token
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "axentx-surrogate-1",
            }
        )
        self.repo_full_name: Optional[str] = None
        self.repo_id: Optional[int] = None

    def _api(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.GITHUB_API_URL}{path}"
        logger.debug("GitHub API request %s %s", method, url)
        response = self.session.request(method, url, **kwargs)
        if not response.ok:
            logger.error(
                "GitHub API error %s %s: %s",
                method,
                url,
                response.text,
            )
            raise GitHubConnectionError(
                f"GitHub API request failed: {response.status_code} {response.text}"
            )
        return response.json()

    def connect(self, repo: str) -> None:
        """
        Verify access to the repository and store its identifier.

        :param repo: Repository in the form ``owner/name``.
        """
        logger.info("Connecting to GitHub repository %s", repo)
        data = self._api("GET", f"/repos/{repo}")
        self.repo_full_name = data["full_name"]
        self.repo_id = data["id"]
        logger.info(
            "Connected to repository %s (id=%s)", self.repo_full_name, self.repo_id
        )

    def register_webhook(
        self,
        webhook_url: str,
        events: List[str],
        secret: Optional[str] = None,
        active: bool = True,
    ) -> Dict[str, Any]:
        """
        Register a webhook on the connected repository.

        :param webhook_url: The URL GitHub will POST events to.
        :param events: List of GitHub event names to subscribe to.
        :param secret: Optional secret for payload signing.
        :param active: Whether the webhook should be active immediately.
        :return: The webhook definition returned by GitHub.
        """
        if not self.repo_full_name:
            raise GitHubConnectionError("Repository not connected. Call connect() first.")

        payload: Dict[str, Any] = {
            "name": "web",
            "active": active,
            "events": events,
            "config": {
                "url": webhook_url,
                "content_type": "json",
                "insecure_ssl": "0",
            },
        }
        if secret:
            payload["config"]["secret"] = secret

        logger.info(
            "Registering webhook for repo %s to %s (events=%s)",
            self.repo_full_name,
            webhook_url,
            events,
        )
        webhook = self._api(
            "POST",
            f"/repos/{self.repo_full_name}/hooks",
            json=payload,
        )
        logger.info("Webhook registered with id %s", webhook.get("id"))
        return webhook

    def handle_event(self, event_payload: Dict[str, Any]) -> None:
        """
        Process an incoming GitHub event payload. Currently this method only logs
        the event; it can be extended to trigger actual workflow automations.

        :param event_payload: The JSON payload received from GitHub.
        """
        event_type = event_payload.get("hook", {}).get("type") or event_payload.get(
            "action"
        )
        logger.info(
            "Received GitHub event %s for repository %s",
            event_type,
            self.repo_full_name or "unknown",
        )
        # Future extension point: dispatch to workflow engine based on event_type.
        # For now we just log the raw payload at DEBUG level.
        logger.debug("Event payload: %s", event_payload)