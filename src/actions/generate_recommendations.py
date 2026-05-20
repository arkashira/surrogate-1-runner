import logging
from typing import List, Dict
from datetime import datetime, timedelta
from ..utils.cost_calculator import CostCalculator

logger = logging.getLogger(__name__)

class RecommendationGenerator:
    def __init__(self):
        self.cost_calculator = CostCalculator()

    def generate_recommendations(self, cost_spike_data: Dict) -> List[Dict]:
        """
        Generate recommendations based on cost spike data.

        Args:
            cost_spike_data: Dictionary containing cost spike information

        Returns:
            List of recommendation dictionaries
        """
        recommendations = []

        # Generate rightsizing recommendations
        rightsizing_rec = self._generate_rightsizing_recommendation(cost_spike_data)
        if rightsizing_rec:
            recommendations.append(rightsizing_rec)

        # Generate shutdown schedule recommendations
        shutdown_rec = self._generate_shutdown_schedule_recommendation(cost_spike_data)
        if shutdown_rec:
            recommendations.append(shutdown_rec)

        return recommendations

    def _generate_rightsizing_recommendation(self, cost_spike_data: Dict) -> Dict:
        """
        Generate rightsizing recommendation based on cost spike data.

        Args:
            cost_spike_data: Dictionary containing cost spike information

        Returns:
            Dictionary containing rightsizing recommendation or None
        """
        # Logic to determine if rightsizing is recommended
        if cost_spike_data['current_cost'] > cost_spike_data['baseline_cost'] * 1.5:
            # Calculate estimated savings and impact duration
            estimated_savings = self.cost_calculator.calculate_rightsizing_savings(
                cost_spike_data['current_cost'],
                cost_spike_data['baseline_cost']
            )
            impact_duration = 30  # days

            return {
                'action': 'rightsizing',
                'description': 'Reduce instance sizes based on current utilization',
                'estimated_savings': estimated_savings,
                'impact_duration': impact_duration,
                'generated_at': datetime.now().isoformat()
            }

        return None

    def _generate_shutdown_schedule_recommendation(self, cost_spike_data: Dict) -> Dict:
        """
        Generate shutdown schedule recommendation based on cost spike data.

        Args:
            cost_spike_data: Dictionary containing cost spike information

        Returns:
            Dictionary containing shutdown schedule recommendation or None
        """
        # Logic to determine if shutdown schedule is recommended
        if cost_spike_data['usage_pattern'] == 'non_prod':
            # Calculate estimated savings and impact duration
            estimated_savings = self.cost_calculator.calculate_shutdown_savings(
                cost_spike_data['current_cost'],
                cost_spike_data['shutdown_hours']
            )
            impact_duration = 30  # days

            return {
                'action': 'shutdown_schedule',
                'description': 'Implement shutdown schedule for non-production resources',
                'estimated_savings': estimated_savings,
                'impact_duration': impact_duration,
                'generated_at': datetime.now().isoformat()
            }

        return None