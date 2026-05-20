"""
App metadata validation endpoint for App Store submission preparation.

Validates:
- App name length (2-30 characters)
- Description length (0-4000 characters)
- Keywords (max 100 chars total, no duplicates, max 10 keywords)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from collections import Counter

router = APIRouter()


class AppMetadata(BaseModel):
    """App metadata to validate."""
    name: str = Field(..., min_length=1, description="App name")
    description: str = Field(..., description="App description")
    keywords: List[str] = Field(default_factory=list, description="App keywords")
    
    @field_validator('keywords', mode='before')
    @classmethod
    def parse_keywords(cls, v):
        """Ensure keywords is a list."""
        if v is None:
            return []
        return v


class FieldValidationResult(BaseModel):
    """Validation result for a single field."""
    field: str
    passed: bool
    error: Optional[str] = None
    
    model_config = {"use_enum_values": True}


class ValidationResponse(BaseModel):
    """Response containing validation results for all fields."""
    overall_passed: bool
    results: List[FieldValidationResult]
    
    model_config = {"use_enum_values": True}


# Validation constants
NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 30
DESCRIPTION_MAX_LENGTH = 4000
KEYWORDS_MAX_TOTAL_LENGTH = 100
KEYWORDS_MAX_COUNT = 10


@router.post("/validate", response_model=ValidationResponse, name="validate_app_metadata")
def validate_app_metadata(metadata: AppMetadata) -> ValidationResponse:
    """
    Validate app metadata for App Store submission.
    
    Returns pass/fail for each field with specific error messages.
    """
    results: List[FieldValidationResult] = []
    
    # ─────────────────────────────────────────────
    # Validate app name (2-30 characters)
    # ─────────────────────────────────────────────
    name = metadata.name.strip()
    name_length = len(name)
    
    if name_length < NAME_MIN_LENGTH:
        results.append(FieldValidationResult(
            field="name",
            passed=False,
            error=f"App name must be at least {NAME_MIN_LENGTH} characters (current: {name_length})"
        ))
    elif name_length > NAME_MAX_LENGTH:
        results.append(FieldValidationResult(
            field="name",
            passed=False,
            error=f"App name must be at most {NAME_MAX_LENGTH} characters (current: {name_length})"
        ))
    else:
        results.append(FieldValidationResult(
            field="name",
            passed=True,
            error=None
        ))
    
    # ─────────────────────────────────────────────
    # Validate description (0-4000 characters)
    # ─────────────────────────────────────────────
    desc_length = len(metadata.description)
    
    if desc_length > DESCRIPTION_MAX_LENGTH:
        results.append(FieldValidationResult(
            field="description",
            passed=False,
            error=f"Description must be at most {DESCRIPTION_MAX_LENGTH} characters (current: {desc_length})"
        ))
    else:
        results.append(FieldValidationResult(
            field="description",
            passed=True,
            error=None
        ))
    
    # ─────────────────────────────────────────────
    # Validate keywords (max 100 chars total, no duplicates, max 10)
    # ─────────────────────────────────────────────
    keywords_concat = "".join(metadata.keywords)
    keywords_length = len(keywords_concat)
    keyword_count = len(metadata.keywords)
    
    # Check for duplicates using Counter (more efficient)
    keyword_counts = Counter(metadata.keywords)
    duplicates = [keyword for keyword, count in keyword_counts.items() if count > 1]
    
    errors = []
    
    if keywords_length > KEYWORDS_MAX_TOTAL_LENGTH:
        errors.append(f"total length must be at most {KEYWORDS_MAX_TOTAL_LENGTH} characters (current: {keywords_length})")
    
    if keyword_count > KEYWORDS_MAX_COUNT:
        errors.append(f"maximum of {KEYWORDS_MAX_COUNT} keywords allowed (current: {keyword_count})")
    
    if duplicates:
        errors.append(f"duplicates found: {', '.join(set(duplicates))}")
    
    if errors:
        results.append(FieldValidationResult(
            field="keywords",
            passed=False,
            error="; ".join(errors)
        ))
    else:
        results.append(FieldValidationResult(
            field="keywords",
            passed=True,
            error=None
        ))
    
    # ─────────────────────────────────────────────
    # Compute overall result
    # ─────────────────────────────────────────────
    overall_passed = all(r.passed for r in results)
    
    return ValidationResponse(
        overall_passed=overall_passed,
        results=results
    )