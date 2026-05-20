import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

import aiohttp
import aiosmtplib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Finding, AlertLog, MutedRule
from .config import SLACK_WEBHOOK_URL, SMTP_SERVER, SMTP_PORT, EMAIL_FROM, EMAIL_TO

logger = logging.getLogger(__name__)

async def send_slack_alert(finding: Finding):
    async with aiohttp.ClientSession() as session:
        payload = {
            "text": f"High Severity Finding: {finding.rule_name} - Resource ID: {finding.resource_id}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*High Severity Finding*\n"
                            f"*Resource ID*: {finding.resource_id}\n"
                            f"*Rule Name*: {finding.rule_name}\n"
                            f"*Severity*: {finding.severity}\n"
                            f"*Dashboard Link*: <{finding.dashboard_link}|View in Dashboard>"
                        ),
                    },
                }
            ],
        }
        async with session.post(SLACK_WEBHOOK_URL, json=payload) as resp:
            return resp.status == 200

async def send_email_alert(finding: Finding):
    message = (
        f"Subject: High Severity Finding - {finding.rule_name}\n\n"
        f"Resource ID: {finding.resource_id}\n"
        f"Rule Name: {finding.rule_name}\n"
        f"Severity: {finding.severity}\n"
        f"Dashboard Link: {finding.dashboard_link}"
    )
    await aiosmtplib.send(
        message,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        sender=EMAIL_FROM,
        recipients=[EMAIL_TO],
    )

async def log_alert_delivery(session: AsyncSession, finding_id: int, success: bool):
    alert_log = AlertLog(finding_id=finding_id, delivered_at=datetime.utcnow(), success=success)
    session.add(alert_log)
    await session.commit()

async def dispatch_alerts(session: AsyncSession, finding: Finding):
    if finding.severity != 'high':
        return

    muted_rule = await session.execute(select(MutedRule).where(MutedRule.rule_name == finding.rule_name))
    if muted_rule.scalar_one_or_none():
        return

    slack_success = await send_slack_alert(finding)
    email_success = await send_email_alert(finding)

    await log_alert_delivery(session, finding.id, slack_success and email_success)

async def main():
    while True:
        # Simulate event subscription logic here
        # For simplicity, we're fetching findings directly from the database
        findings = await session.execute(select(Finding).where(Finding.created_at >= datetime.utcnow() - timedelta(minutes=2)))
        for finding in findings.scalars():
            await dispatch_alerts(session, finding)
        await asyncio.sleep(120)  # Check every 2 minutes

if __name__ == "__main__":
    asyncio.run(main())