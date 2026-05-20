import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SlackConfig:
    """Configuration required for Slack notifications.

    Values are read from environment variables at import time.
    """

    bot_token: str
    channel: str
    default_channel: Optional[str] = None
    username: str = "surrogate-1-bot"
    icon_emoji: str = ":robot_face:"

    @staticmethod
    def load_from_env() -> "SlackConfig":
        """Load Slack configuration from environment variables.

        Required:
            SLACK_BOT_TOKEN – Bot token for the target workspace.
            SLACK_CHANNEL – Default channel for messages.

        Optional:
            SLACK_DEFAULT_CHANNEL – Channel name (e.g. "#ingest-status").
            SLACK_BOT_USERNAME – Username to display for messages.
            SLACK_BOT_ICON_EMOJI – Emoji icon for the bot.
        """
        bot_token = os.getenv("SLACK_BOT_TOKEN")
        channel = os.getenv("SLACK_CHANNEL")
        if not bot_token or not channel:
            missing_vars = []
            if not bot_token:
                missing_vars.append("SLACK_BOT_TOKEN")
            if not channel:
                missing_vars.append("SLACK_CHANNEL")
            raise ValueError(f"Environment variables {', '.join(missing_vars)} must be set for Slack integration.")

        return SlackConfig(
            bot_token=bot_token,
            channel=channel,
            default_channel=os.getenv("SLACK_DEFAULT_CHANNEL"),
            username=os.getenv("SLACK_BOT_USERNAME", "surrogate-1-bot"),
            icon_emoji=os.getenv("SLACK_BOT_ICON_EMOJI", ":robot_face:"),
        )