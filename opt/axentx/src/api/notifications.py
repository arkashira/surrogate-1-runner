from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl
from src.notifications.slack_notifier import SlackNotifier

router = APIRouter()

class SlackConfig(BaseModel):
    webhook_url: HttpUrl  # Using HttpUrl for better URL validation

@router.post("/slack", status_code=status.HTTP_201_CREATED)
async def configure_slack_notifications(config: SlackConfig):
    """Configure Slack webhook URL (in production, this would store securely)"""
    # In a real application, you would store the webhook URL securely
    # For this example, we'll just validate the URL and return success
    return {"message": "Slack webhook URL configured successfully"}

@router.post("/slack/test", status_code=status.HTTP_200_OK)
async def test_slack_notification(config: SlackConfig):
    """Test Slack notification delivery"""
    notifier = SlackNotifier(str(config.webhook_url))
    success = notifier.send_test_notification()

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test notification"
        )
    return {"message": "Test notification sent successfully"}