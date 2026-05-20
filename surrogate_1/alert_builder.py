"""
Utility for building Slack alert messages.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AlertConfig:
    include_anomaly_details: bool = True
    include_forecast_summary: bool = True
    top_recommendations_count: int = 3
    minimum_severity: str = "warning"


@dataclass
class AnomalyData:
    anomaly_type: str
    severity: str
    value: float
    expected: float
    forecast_daily: float
    forecast_monthly: float
    trend: str
    recommendations: List[str] = field(default_factory=list)


class AlertBuilder:
    """Builds a Slack message from anomaly data and config."""

    SEVERITY_ORDER = {"info": 0, "warning": 1, "critical": 2}

    def __init__(self, config: AlertConfig):
        self.config = config

    def _severity_ok(self, severity: str) -> bool:
        """Return True if severity meets the minimum threshold."""
        return self.SEVERITY_ORDER.get(severity.lower(), 0) >= \
               self.SEVERITY_ORDER.get(self.config.minimum_severity.lower(), 0)

    def build(self, data: AnomalyData) -> str | None:
        """Return a Slack message or None if severity is too low."""
        if not self._severity_ok(data.severity):
            return None

        parts: List[str] = []

        if self.config.include_anomaly_details:
            parts.extend(
                [
                    "🚨 *Anomaly Detected*",
                    f"• Type: {data.anomaly_type}",
                    f"• Severity: {data.severity}",
                    f"• Value: ${data.value:,.2f}",
                    f"• Expected: ${data.expected:,.2f}",
                ]
            )

        if self.config.include_forecast_summary:
            parts.extend(
                [
                    "\n📊 *Forecast Summary*",
                    f"• Projected daily spend: ${data.forecast_daily:,.2f}",
                    f"• Projected monthly spend: ${data.forecast_monthly:,.2f}",
                    f"• Trend: {data.trend}",
                ]
            )

        top_n = self.config.top_recommendations_count
        if top_n > 0 and data.recommendations:
            parts.append(f"\n💡 *Top {top_n} Recommendations*")
            for i, rec in enumerate(data.recommendations[:top_n], 1):
                parts.append(f"{i}. {rec}")

        return "\n".join(parts)