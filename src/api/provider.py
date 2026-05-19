import os
import uuid
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

import smtplib
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, Field, validator
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from config import settings

Base = declarative_base()

class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    website = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=False)  # Changed to False until verified
    password_hash = Column(String)  # Store hashed password

class ProviderRegistration(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., email=True)
    website: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    password: str = Field(..., min_length=8)

    @validator('email')
    def validate_email_format(cls, v):
        """Validate email format and domain"""
        if not v.endswith('@example.com'):
            raise ValueError('Email must end with @example.com')
        return v

class ProviderRegistrationResponse(BaseModel):
    provider_id: str
    message: str

router = APIRouter()

def get_db():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def send_confirmation_email(email: str, provider_id: str):
    """Send confirmation email with verification link"""
    try:
        msg = MIMEMultipart()
        msg['From'] = 'noreply@axentx.com'
        msg['To'] = email
        msg['Subject'] = 'Welcome to Axentx Provider Network'

        body = f"""
        Thank you for registering as a provider with Axentx.

        Your provider ID: {provider_id}

        Please verify your account by clicking on the link below:
        https://axentx.com/verify/{provider_id}

        Best regards,
        The Axentx Team
        """
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send confirmation email. Please try again later."
        )

@router.post(
    "/register",
    response_model=ProviderRegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_provider(provider_data: ProviderRegistration = Body(...)):
    db = next(get_db())

    try:
        # Check if provider already exists
        existing_provider = db.query(Provider).filter(
            Provider.email == provider_data.email
        ).first()
        if existing_provider:
            raise HTTPException(
                status_code=400,
                detail="Provider with this email already exists"
            )

        # Create new provider with hashed password
        provider = Provider(
            provider_id=str(uuid.uuid4()),
            name=provider_data.name,
            email=provider_data.email,
            website=provider_data.website,
            description=provider_data.description,
            password_hash=generate_password_hash(provider_data.password),
            is_active=False  # Requires email verification
        )

        db.add(provider)
        db.commit()
        db.refresh(provider)

        # Send confirmation email
        send_confirmation_email(provider.email, provider.provider_id)

        return ProviderRegistrationResponse(
            provider_id=provider.provider_id,
            message="Provider registered successfully. Confirmation email sent."
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/providers/{provider_id}")
def get_provider(provider_id: str):
    db = next(get_db())
    provider = db.query(Provider).filter(Provider.provider_id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.post("/verify/{provider_id}")
async def verify_provider(provider_id: str):
    """Endpoint for email verification"""
    db = next(get_db())
    provider = db.query(Provider).filter(Provider.provider_id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    if provider.is_active:
        raise HTTPException(status_code=400, detail="Provider already verified")

    provider.is_active = True
    db.commit()

    return {"message": "Provider verified successfully"}