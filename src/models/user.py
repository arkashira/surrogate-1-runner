from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

Base = declarative_base()

class UserDB(Base):  # Database model
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    email_alerts = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name}, email_alerts={self.email_alerts})>"

class User(BaseModel):  # Pydantic model for API/validation
    id: Optional[int] = None
    email: EmailStr
    name: Optional[str] = None
    email_alerts: bool = True

    @validator('email')
    def email_must_be_valid(cls, v):
        if not v:
            raise ValueError('Email cannot be empty')
        return v

# src/services/email.py
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from typing import Dict

# Rate limiting storage (in-memory for simplicity; consider Redis in production)
last_alert_times: Dict[str, datetime] = {}

def send_email(user: User, pipeline_name: str, error_snippet: str):
    if not user.email_alerts:
        return

    # Rate limiting: 1 alert per pipeline per hour
    key = f"{user.email}_{pipeline_name}"
    if key in last_alert_times and (datetime.now() - last_alert_times[key]) < timedelta(hours=1):
        return

    msg = EmailMessage()
    msg.set_content(
        f'Pipeline {pipeline_name} failed with error:\n{error_snippet}\n'
        f'Visit your dashboard for more details.'
    )
    msg['Subject'] = 'Axentx Pipeline Failure Alert'
    msg['From'] = 'alerts@axentx.com'
    msg['To'] = user.email

    try:
        with smtplib.SMTP('smtp.example.com') as server:
            server.send_message(msg)
        last_alert_times[key] = datetime.now()
    except Exception as e:
        print(f"Failed to send email: {e}")

# src/services/ingestion.py
from src.services.email import send_email
from src.models.user import User
import time

def ingestion_job(user: User, pipeline_name: str):
    try:
        # Ingestion logic here
        pass
    except Exception as e:
        error_snippet = str(e)[:200]  # Limit error snippet length
        send_email(user, pipeline_name, error_snippet)
        time.sleep(3600)  # Wait for an hour before retrying