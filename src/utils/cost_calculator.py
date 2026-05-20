import logging
from typing import Dict

logger = logging.getLogger(__name__)

class CostCalculator:
    def calculate_rightsizing_savings(self, current_cost: float, baseline_cost: float) -> float:
        """
        Calculate estimated savings from rightsizing.

        Args:
            current_cost: Current cost
            baseline_cost: Baseline cost

        Returns:
            Estimated savings
        """
        if current_cost <= baseline_cost:
            return 0.0

        return current_cost - baseline_cost

    def calculate_shutdown_savings(self, current_cost: float, shutdown_hours: int) -> float:
        """
        Calculate estimated savings from shutdown schedule.

        Args:
            current_cost: Current cost
            shutdown_hours: Number of hours resources will be shut down per week

        Returns:
            Estimated savings
        """
        if shutdown_hours <= 0:
            return 0.0

        daily_cost = current_cost / 24
        weekly_savings = daily_cost * shutdown_hours
        monthly_savings = weekly_savings * 4

        return monthly_savings