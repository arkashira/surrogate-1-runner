import logging
from typing import Dict, Any
from src.observability import ObservabilityClient

class RootCauseDiagnostics:
    def __init__(self, observability_client: ObservabilityClient):
        self.observability_client = observability_client
        self.logger = logging.getLogger(__name__)

    def analyze_deviation(self, deviation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the deviation and provide root cause diagnostics.

        Args:
            deviation_data: Data about the deviation detected.

        Returns:
            A dictionary containing root cause diagnostics.
        """
        try:
            # Use observability tools to gather metrics and logs
            metrics = self.observability_client.get_metrics(deviation_data['metric_id'])
            logs = self.observability_client.get_logs(deviation_data['log_query'])

            # Analyze the metrics and logs to determine the root cause
            root_cause = self._determine_root_cause(metrics, logs)

            return {
                'deviation_id': deviation_data['id'],
                'root_cause': root_cause,
                'metrics': metrics,
                'logs': logs
            }
        except Exception as e:
            self.logger.error(f"Error analyzing deviation: {e}")
            raise

    def _determine_root_cause(self, metrics: Dict[str, Any], logs: Dict[str, Any]) -> str:
        """
        Determine the root cause based on metrics and logs.

        Args:
            metrics: Metrics data.
            logs: Logs data.

        Returns:
            A string describing the root cause.
        """
        # Example logic to determine root cause
        if metrics['error_rate'] > 0.1:
            return "High error rate detected"
        elif logs['critical_errors'] > 10:
            return "Multiple critical errors in logs"
        else:
            return "Root cause could not be determined"