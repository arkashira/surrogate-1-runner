"""
App metadata validators for App Store submission validation.

Validates:
- App name: 2-30 characters
- Description: 0-4000 characters  
- Keywords: max 100 chars, no duplicates, comma/semicolon/space separated
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class ValidationResult:
    """Result of a single field validation."""
    field: str
    passed: bool
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        result = {"field": self.field, "passed": self.passed}
        if self.error_message:
            result["error_message"] = self.error_message
        return result


class MetadataValidator:
    """Validator for app metadata fields."""

    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 30
    DESCRIPTION_MAX_LENGTH = 4000
    KEYWORDS_MAX_LENGTH = 100

    def validate_name(self, name: str) -> ValidationResult:
        """Validate app name length (2-30 characters)."""
        if not isinstance(name, str):
            return ValidationResult(
                field="name",
                passed=False,
                error_message="App name must be a string"
            )
        
        length = len(name)
        
        if length < self.NAME_MIN_LENGTH:
            return ValidationResult(
                field="name",
                passed=False,
                error_message=f"App name must be at least {self.NAME_MIN_LENGTH} characters (got {length})"
            )
        
        if length > self.NAME_MAX_LENGTH:
            return ValidationResult(
                field="name",
                passed=False,
                error_message=f"App name must be at most {self.NAME_MAX_LENGTH} characters (got {length})"
            )
        
        return ValidationResult(field="name", passed=True)

    def validate_description(self, description: str) -> ValidationResult:
        """Validate description length (0-4000 characters)."""
        if not isinstance(description, str):
            return ValidationResult(
                field="description",
                passed=False,
                error_message="Description must be a string"
            )
        
        length = len(description)
        
        if length > self.DESCRIPTION_MAX_LENGTH:
            return ValidationResult(
                field="description",
                passed=False,
                error_message=f"Description must be at most {self.DESCRIPTION_MAX_LENGTH} characters (got {length})"
            )
        
        return ValidationResult(field="description", passed=True)

    def validate_keywords(self, keywords: str) -> ValidationResult:
        """Validate keywords (max 100 chars, no duplicates)."""
        if not isinstance(keywords, str):
            return ValidationResult(
                field="keywords",
                passed=False,
                error_message="Keywords must be a string"
            )
        
        length = len(keywords)
        
        if length > self.KEYWORDS_MAX_LENGTH:
            return ValidationResult(
                field="keywords",
                passed=False,
                error_message=f"Keywords must be at most {self.KEYWORDS_MAX_LENGTH} characters (got {length})"
            )
        
        if keywords:
            # Split by comma, semicolon, or whitespace
            parts = re.split(r'[,;]\s*|\s+', keywords.strip())
            parts = [p for p in parts if p]  # Filter empty
            
            # Check duplicates (case-insensitive)
            unique_parts = set(p.lower() for p in parts)
            
            if len(parts) != len(unique_parts):
                return ValidationResult(
                    field="keywords",
                    passed=False,
                    error_message="Keywords contain duplicates"
                )
        
        return ValidationResult(field="keywords", passed=True)

    def validate_all(self, name: str, description: str, keywords: str) -> dict:
        """Validate all metadata fields."""
        return {
            "name": self.validate_name(name).to_dict(),
            "description": self.validate_description(description).to_dict(),
            "keywords": self.validate_keywords(keywords).to_dict()
        }