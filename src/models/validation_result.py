from typing import List, Optional
from dataclasses import dataclass, field
from .control import Control


@dataclass
class ValidationResult:
    """Result of a control validation operation."""

    success: bool
    missing_controls: List[Control] = field(default_factory=list)

    def __str__(self) -> str:
        """Human-readable representation of the validation result."""
        if self.success:
            return "✓ Validation successful: All controls are addressed."
        
        missing_ids = [c.id for c in self.missing_controls]
        return f"✗ Validation failed: Missing {len(missing_ids)} control(s) - {missing_ids}"

    @property
    def missing_count(self) -> int:
        """Returns the count of missing controls."""
        return len(self.missing_controls)

    def to_dict(self) -> dict:
        """Converts the result to a dictionary."""
        return {
            'success': self.success,
            'missing_control_ids': [c.id for c in self.missing_controls],
            'missing_count': self.missing_count
        }