from datetime import datetime
from typing import List
from src.models.cost_event import CostEvent

class AlertManager:
    """Manages alerting for cost anomalies."""
    
    def __init__(self):
        self.alert_handlers = []
        self.last_alert_time = {}
        
    def add_alert_handler(self, handler_func):
        """Add a function to handle alerts."""
        self.alert_handlers.append(handler_func)
        
    def trigger_alert(self, cost_event: CostEvent):
        """Trigger alerts for a cost event."""
        # Rate limiting - don't alert more than once per hour
        provider = cost_event.provider
        now = datetime.now()
        
        if provider in self.last_alert_time:
            time_since_last = now - self.last_alert_time[provider]
            if time_since_last < timedelta(hours=1):
                return  # Don't send too many alerts
                
        self.last_alert_time[provider] = now
        
        # Format alert data
        alert_data = {
            'provider': cost_event.provider,
            'cost_delta': cost_event.cost_delta,
            'timestamp': cost_event.timestamp,
            'current_cost': cost_event.current_cost,
            'baseline_cost': cost_event.baseline_cost
        }
        
        # Send to all handlers
        for handler in self.alert_handlers:
            try:
                handler(alert_data)
            except Exception as e:
                print(f"Error in alert handler: {e}")
                
    def configure_alerts(self, config: dict):
        """Configure alert settings via UI/API."""
        # This method would be extended to support configuration
        pass