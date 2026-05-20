import yaml
import statistics
import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CostMonitor:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.slack_webhook = self.config.get('slack_webhook')
        self.teams_webhook = self.config.get('teams_webhook')
        self.threshold_multiplier = self.config.get('threshold_multiplier', 3)
        self.lookback_days = self.config.get('lookback_days', 7)
        
        logger.info(f"CostMonitor initialized with {self.lookback_days} day lookback, "
                   f"{self.threshold_multiplier}σ threshold")

    def get_cost_data(self):
        """
        Retrieve cost data from cloud provider.
        Replace placeholder with actual API calls:
        - AWS: boto3 + Cost Explorer API
        - GCP: cloud billing BigQuery export
        - Azure: Cost Management API
        """
        # Example: return list of (date, cost) tuples for last N days
        base_costs = [100, 105, 110, 115, 120, 125, 130]
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') 
                 for i in range(len(base_costs)-1, -1, -1)]
        return list(zip(dates, base_costs))

    def detect_anomalies(self, cost_data):
        """Detect anomalies using z-score method."""
        costs = [cost for _, cost in cost_data]
        
        if len(costs) < 2:
            logger.warning("Insufficient data for anomaly detection")
            return [], 0, 0
        
        mean = statistics.mean(costs)
        stdev = statistics.stdev(costs)
        threshold = mean + (self.threshold_multiplier * stdev)
        
        anomalies = []
        for date, cost in cost_data:
            if cost > threshold:
                z_score = (cost - mean) / stdev if stdev > 0 else 0
                anomalies.append({
                    'date': date,
                    'cost': cost,
                    'z_score': round(z_score, 2),
                    'deviation': round(cost - mean, 2)
                })
                logger.warning(f"Anomaly detected: {date} = ${cost} (z={z_score:.2f})")
        
        return anomalies, mean, stdev

    def send_alert(self, message):
        """Send alert to configured webhooks with error handling."""
        payload = {'text': message}
        
        if self.slack_webhook:
            try:
                response = requests.post(self.slack_webhook, json=payload, timeout=10)
                response.raise_for_status()
                logger.info("Slack alert sent successfully")
            except requests.RequestException as e:
                logger.error(f"Failed to send Slack alert: {e}")
        
        if self.teams_webhook:
            try:
                response = requests.post(self.teams_webhook, json=payload, timeout=10)
                response.raise_for_status()
                logger.info("Teams alert sent successfully")
            except requests.RequestException as e:
                logger.error(f"Failed to send Teams alert: {e}")

    def generate_recommendations(self, anomalies):
        """Generate actionable recommendations based on anomaly patterns."""
        recommendations = []
        
        for anomaly in anomalies:
            if anomaly['z_score'] > 4:
                recommendations.append(f"CRITICAL: {anomaly['date']} cost ${anomaly['cost']} "
                                        f"is {anomaly['z_score']}σ above mean - immediate investigation required")
            elif anomaly['z_score'] > 3:
                recommendations.append(f"WARNING: {anomaly['date']} cost ${anomaly['cost']} "
                                        f"exceeds 3σ threshold - review recent deployments")
        
        # General recommendations
        recommendations.extend([
            "Check for unexpected usage spikes in the last 24-48 hours",
            "Review recent infrastructure changes or deployments",
            "Verify no runaway processes or misconfigured resources"
        ])
        
        return recommendations

    def run(self):
        """Main execution loop."""
        logger.info("Starting cost anomaly detection")
        
        cost_data = self.get_cost_data()
        anomalies, mean, stdev = self.detect_anomalies(cost_data)
        
        if anomalies:
            message = f"🚨 *Cost Anomaly Detected*\n\n"
            message += f"• Mean: ${mean:.2f}\n"
            message += f"• Std Dev: ${stdev:.2f}\n"
            message += f"• Threshold: ${mean + (self.threshold_multiplier * stdev):.2f}\n\n"
            message += "*Anomalies:*\n"
            
            for a in anomalies:
                message += f"• {a['date']}: ${a['cost']} (z={a['z_score']})\n"
            
            message += "\n*Recommendations:*\n"
            for rec in self.generate_recommendations(anomalies):
                message += f"• {rec}\n"
            
            self.send_alert(message)
        else:
            logger.info("No anomalies detected")

if __name__ == "__main__":
    monitor = CostMonitor('/opt/axentx/surrogate-1/config/anomaly_rules.yaml')
    monitor.run()