import datetime
from typing import Dict, List, Optional, Tuple

class CostAnomalyDetector:
    """
    Detects cost anomalies using a 3-sigma rule on daily cost totals per service.
    An anomaly is flagged if the current day's total deviates more than 3 standard
    deviations from the historical mean.
    """

    def __init__(self, historical_data: Dict[str, List[float]]):
        """
        Initializes the detector with historical daily cost data per service.

        Args:
            historical_data: Mapping from service identifier to list of daily totals.
                             The list should contain totals for the past 7 days.
        """
        self.historical_data = historical_data

    def _calculate_statistics(self, daily_totals: List[float]) -> Tuple[Optional[float], Optional[float]]:
        """
        Calculates the mean and standard deviation of a list of daily totals.

        Args:
            daily_totals: List of daily cost totals.

        Returns:
            A tuple (mean, std) or (None, None) if the list is empty.
        """
        if not daily_totals:
            return None, None
        mean = sum(daily_totals) / len(daily_totals)
        variance = sum((x - mean) ** 2 for x in daily_totals) / len(daily_totals)
        std = variance ** 0.5
        return mean, std

    def detect_anomalies(self, current_daily_totals: Dict[str, float]) -> List[Dict[str, any]]:
        """
        Detects anomalies based on the 3-sigma rule.

        Args:
            current_daily_totals: Mapping from service identifier to current day's total.

        Returns:
            List of anomaly dictionaries with the required fields.
        """
        anomalies = []
        for service, current_total in current_daily_totals.items():
            mean, std = self._calculate_statistics(self.historical_data.get(service, []))
            if mean is None or std is None:
                continue  # Not enough historical data for this service
            deviation = (current_total - mean) / std
            if abs(deviation) > 3:
                anomalies.append({
                    'provider': service.get('provider', 'unknown'),
                    'service': service.get('service', 'unknown'),
                    'amount_usd': current_total,
                    'baseline_usd': mean,
                    'deviation_pct': abs(deviation) * 100,
                    'timestamp': datetime.datetime.now().isoformat()
                })
        return anomalies