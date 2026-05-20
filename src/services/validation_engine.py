import logging
from typing import List, Dict, Optional
from models.validation_result import ValidationResult
from models.control import Control


class ValidationEngine:
    """Engine for validating that infrastructure components address required controls."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the ValidationEngine.

        Args:
            logger: Optional logger instance. If not provided, creates one.
        """
        self.logger = logger or logging.getLogger(__name__)

    def validate_controls(
        self,
        infrastructure_components: List[Dict],
        controls: List[Control]
    ) -> ValidationResult:
        """
        Validates that all critical controls are addressed in the infrastructure components.

        Args:
            infrastructure_components: List of infrastructure components with their configurations.
                                         Each component should have an 'addressed_controls' key containing
                                         a list of control IDs it addresses.
            controls: List of controls that need to be validated.

        Returns:
            ValidationResult: Result of the validation including missing controls.
        """
        if not infrastructure_components:
            self.logger.warning("No infrastructure components provided for validation.")
            return ValidationResult(
                success=False,
                missing_controls=list(controls)
            )

        if not controls:
            self.logger.info("No controls to validate.")
            return ValidationResult(success=True, missing_controls=[])

        missing_controls = [
            control for control in controls
            if not self._is_control_addressed(infrastructure_components, control)
        ]

        if missing_controls:
            missing_ids = [c.id for c in missing_controls]
            self.logger.warning(f"Validation failed. Missing controls: {missing_ids}")
            return ValidationResult(success=False, missing_controls=missing_controls)

        self.logger.info("Validation successful: All controls are addressed.")
        return ValidationResult(success=True, missing_controls=[])

    def _is_control_addressed(
        self,
        infrastructure_components: List[Dict],
        control: Control
    ) -> bool:
        """
        Checks if a specific control is addressed in any infrastructure component.

        Args:
            infrastructure_components: List of infrastructure components with their configurations.
            control: Control to check.

        Returns:
            bool: True if the control is addressed by any component, False otherwise.
        """
        for component in infrastructure_components:
            addressed = component.get('addressed_controls', [])
            if control.id in addressed:
                return True
        return False

    def get_addressed_controls(
        self,
        infrastructure_components: List[Dict]
    ) -> List[str]:
        """
        Extracts all control IDs that are addressed by the infrastructure.

        Args:
            infrastructure_components: List of infrastructure components.

        Returns:
            List of unique control IDs that are addressed.
        """
        addressed = set()
        for component in infrastructure_components:
            addressed.update(component.get('addressed_controls', []))
        return list(addressed)