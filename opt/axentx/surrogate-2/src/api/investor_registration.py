from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr, ValidationError
from typing import List

from .. import db
from ..schemas.investor_schema import InvestorCreate, InvestorOut, InvestorUpdate
from ..models.investor import Investor
from ..utils.auth import get_current_user, verify_password, create_access_token
from ..utils.validators import validate_email, validate_password, validate_required_fields

router = APIRouter(prefix="/investors", tags=["investors"])

# Dependency to get DB session
def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/register", response_model=InvestorOut)
def register_investor(
    investor_data: InvestorCreate,
    db: Session = Depends(get_db),
):
    # Validate required fields
    required_fields = ['email', 'password', 'firm_name', 'investment_stage', 'ticket_size', 'focus_areas', 'geographic_preference']
    if not validate_required_fields(investor_data.dict(), required_fields):
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Validate email
    if not validate_email(investor_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Validate password
    if not validate_password(investor_data.password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number")

    # Check if investor already exists
    if Investor.query.filter_by(email=investor_data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create new investor
    hashed_password = verify_password(investor_data.password)
    new_investor = Investor(
        email=investor_data.email,
        password=hashed_password,
        firm_name=investor_data.firm_name,
        investment_stage=investor_data.investment_stage,
        ticket_size=investor_data.ticket_size,
        focus_areas=investor_data.focus_areas,
        geographic_preference=investor_data.geographic_preference
    )

    db.add(new_investor)
    db.commit()
    db.refresh(new_investor)

    return new_investor