
import asyncio
import json
import logging
import time
from typing import Dict, Any
from urllib.parse import urlparse
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, validator
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas, database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/notifications/slack", tags=["slack"])

class SlackConfig(BaseModel):
    webhook_url: str

    @validator("webhook_url")
    def validate_webhook_url(cls, v):
        if not v:
            raise ValueError("Webhook URL cannot be empty")
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid webhook URL format")
        return v

class Violation(BaseModel):
    id: str
    title: str
    severity: str
    description: str
    timestamp: str

async def send_slack_notification(webhook_url: str, payload: Dict[str, Any]) -> bool:
    """Send notification to Slack webhook with retry logic."""
    max_retries = 3
    base_delay = 1  # seconds
    
    for attempt in range(max_retries + 1):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        logger.info(f"Successfully sent Slack notification (attempt {attempt + 1})")
                        return True
                    else:
                        logger.warning(
                            f"Slack webhook failed (status {response.status}) "
                            f"(attempt {attempt + 1})"
                        )
        except Exception as e:
            logger.warning(
                f"Failed to send Slack notification (attempt {attempt + 1}): {str(e)}"
            )
        
        if attempt < max_retries:
            delay = base_delay * (2 ** attempt)
            logger.info(f"Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
    
    logger.error("All retry attempts failed for Slack webhook")
    return False

@router.post("", status_code=status.HTTP_201_CREATED)
async def configure_slack_webhook(config: SlackConfig, db: Session = Depends(database.get_db)):
    """
    Configure Slack webhook URL for notifications.
    
    Args:
        config: Slack webhook configuration containing the URL
        
    Returns:
        Success response with configured webhook URL
    """
    # Save the configuration to the database
    db_config = models.SlackConfig(webhook_url=config.webhook_url)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    # Get the high-severity violation
    violation = await models.Violation.get_high_severity(db)
    
    if not violation:
        return {"message": "No high severity violations found."}
    
    # Send the notification
    message = f"High severity violation detected:\n{violation.description}"
    if await send_slack_notification(config.webhook_url, {"text": message}):
        return {"message": "Slack notification sent."}
    else:
        return {"message": "Failed to send Slack notification."}

# src/tests/test_slack.py

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app, oauth2_scheme
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session

Base = declarative_base()

class TestSlack(unittest.IsolatedAsyncioTestCase):
    async def setUp(self):
        self.client = TestClient(app)
        self.db = create_session()
        Base.metadata.create_all(engine)

    async def tearDown(self):
        self.db.close()

    @patch("aiohttp.ClientSession")
    async def test_slack_webhook(self, mock_session):
        mock_session.return_value.post.return_value.__aenter__.return_value.status = 200
        
        response = await self.client.post("/api/v1/notifications/slack", data={"webhook_url": "https://hooks.slack.com/services/..."})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Slack notification sent."})

    @patch("aiohttp.ClientSession")
    async def test_slack_webhook_failure(self, mock_session):
        mock_session.return_value.post.side_effect = Exception("Mocked exception")
        
        response = await self.client.post("/api/v1/notifications/slack", data={"webhook_url": "https://hooks.slack.com/services/..."})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Failed to send Slack notification."})