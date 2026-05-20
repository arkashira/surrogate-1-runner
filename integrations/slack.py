import os
import json
import logging
from urllib import request, error
from typing import Any, Dict, List, Optional

# Optional async support – only imported when needed so the package has no hard
# dependency on httpx.
try:
    import httpx  # type: ignore
except Exception:  # pragma: no cover
    httpx = None  # noqa: N816

logger = logging.getLogger(__name__)


class SlackSyncNotifier:
    """
    Synchronous Slack notifier that posts to an Incoming Webhook.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError(
                "Slack webhook URL must be provided via argument or SLACK_WEBHOOK_URL env var"
            )

    def send(self, text: str, blocks: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Send a message to Slack.

        Returns ``True`` if Slack responded with a 2xx status code, ``False`` otherwise.
        """
        payload: Dict[str, Any] = {"text": text}
        if blocks:
            payload["blocks"] = blocks

        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode()
                if 200 <= resp.getcode() < 300:
                    logger.info("Slack notification sent successfully (sync).")
                    return True
                logger.error(
                    "Slack notification failed (sync). Status: %s, Body: %s",
                    resp.getcode(),
                    body,
                )
                return False
        except error.URLError as exc:
            logger.exception("Error sending Slack notification (sync): %s", exc)
            return False


class SlackAsyncNotifier:
    """
    Optional asynchronous Slack notifier built on httpx.
    Instantiated only when ``httpx`` is available.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        if httpx is None:  # pragma: no cover
            raise RuntimeError("httpx is required for async Slack notifications")
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError(
                "Slack webhook URL must be provided via argument or SLACK_WEBHOOK_URL env var"
            )

    async def send(self, text: str, blocks: Optional[List[Dict[str, Any]]] = None) -> None:
        payload: Dict[str, Any] = {"text": text}
        if blocks:
            payload["blocks"] = blocks

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    self.webhook_url, json=payload, timeout=10.0
                )
                resp.raise_for_status()
                logger.info("Slack notification sent successfully (async).")
            except Exception as exc:  # pragma: no cover
                logger.error("Failed to send Slack notification (async): %s", exc)
                raise