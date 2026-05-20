import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class AlertSystem:
    def __init__(self, config_file: str = "/opt/axentx/surrogate-1/config/alert_config.json"):
        """
        Initialize AlertSystem with configurable thresholds.

        Args:
            config_file: Path to JSON configuration file
        """
        self.config_file = config_file
        self.alerts_config = self._load_config()
        self.alerts: List[Dict[str, Any]] = []

    def _load_config(self) -> Dict[str, Any]:
        """Load alert configuration with sensible defaults."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "thresholds": [
                    {"name": "high_cost", "value": 1000, "enabled": True},
                    {"name": "medium_cost", "value": 500, "enabled": True}
                ],
                "default_savings_estimate": 200,
                "customizable_alerts": True
            }

    def check_cost_thresholds(self, current_cost: float) -> List[Dict[str, Any]]:
        """
        Check if current cost exceeds any configured thresholds.

        Args:
            current_cost: Current cloud cost to evaluate

        Returns:
            List of alert dictionaries for exceeded thresholds
        """
        alerts = []
        for threshold in self.alerts_config.get("thresholds", []):
            if threshold.get("enabled", False) and current_cost >= threshold["value"]:
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "threshold_name": threshold["name"],
                    "threshold_value": threshold["value"],
                    "current_cost": current_cost,
                    "estimated_savings": self._calculate_savings(current_cost),
                    "message": self._generate_message(threshold["name"], current_cost)
                }
                alerts.append(alert)
                self.alerts.append(alert)
        return alerts

    def _calculate_savings(self, current_cost: float) -> float:
        """Calculate estimated savings (10% of current cost by default)."""
        return round(current_cost * 0.1, 2)

    def _generate_message(self, threshold_name: str, current_cost: float) -> str:
        """Generate appropriate alert message based on threshold."""
        messages = {
            "high_cost": f"High cloud cost detected: ${current_cost:.2f}. Consider optimizing resources.",
            "medium_cost": f"Medium cloud cost detected: ${current_cost:.2f}. Review usage patterns."
        }
        return messages.get(threshold_name, f"Cost threshold exceeded: ${current_cost:.2f}")

    def save_alerts(self, file_path: Optional[str] = None) -> bool:
        """
        Save alerts to JSON file.

        Args:
            file_path: Optional custom file path (defaults to config location)

        Returns:
            True if successful, False otherwise
        """
        try:
            path = file_path or os.path.join(
                os.path.dirname(self.config_file),
                "alert_history.json"
            )
            with open(path, 'w') as f:
                json.dump(self.alerts, f, indent=2)
            return True
        except Exception:
            return False

    def load_alerts(self, file_path: Optional[str] = None) -> bool:
        """
        Load alerts from JSON file.

        Args:
            file_path: Optional custom file path (defaults to config location)

        Returns:
            True if successful, False otherwise
        """
        try:
            path = file_path or os.path.join(
                os.path.dirname(self.config_file),
                "alert_history.json"
            )
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self.alerts = json.load(f)
                return True
            return False
        except Exception:
            return False

    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """Update configuration and save to file."""
        try:
            self.alerts_config.update(new_config)
            with open(self.config_file, 'w') as f:
                json.dump(self.alerts_config, f, indent=2)
            return True
        except Exception:
            return False