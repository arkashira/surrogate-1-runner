import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from src.models.cost_event import CostEvent
from src.utils.alert_manager import AlertManager

class CostAnalyzer:
    def __init__(self, alert_manager: AlertManager):
        self.alert_manager = alert_manager
        self.cost_history = []
        self.anomaly_threshold = 2.0  # Standard deviations above mean
        
    def detect_cost_anomalies(self, current_costs: Dict[str, float]) -> List[CostEvent]:
        """
        Detect cost anomalies by comparing current costs against historical data.
        
        Args:
            current_costs: Dictionary mapping provider names to current cost values
            
        Returns:
            List of CostEvent objects representing detected anomalies
        """
        anomalies = []
        
        # Update history with current costs
        self.cost_history.append({
            'timestamp': datetime.now(),
            'costs': current_costs.copy()
        })
        
        # Keep only last 30 entries for analysis
        if len(self.cost_history) > 30:
            self.cost_history.pop(0)
            
        # For each provider, check if current cost is anomalous
        for provider, current_cost in current_costs.items():
            provider_costs = [entry['costs'].get(provider, 0) 
                            for entry in self.cost_history]
            
            if len(provider_costs) < 5:  # Need at least 5 data points
                continue
                
            # Calculate statistics
            mean_cost = np.mean(provider_costs)
            std_cost = np.std(provider_costs)
            
            # Skip if standard deviation is too small
            if std_cost < 0.01:
                continue
                
            # Calculate z-score
            z_score = (current_cost - mean_cost) / std_cost
            
            # Check if it's an anomaly (more than 2 standard deviations)
            if abs(z_score) > self.anomaly_threshold:
                # Calculate cost delta
                cost_delta = current_cost - mean_cost
                
                # Create cost event
                cost_event = CostEvent(
                    provider=provider,
                    current_cost=current_cost,
                    baseline_cost=mean_cost,
                    cost_delta=cost_delta,
                    timestamp=datetime.now(),
                    anomaly_z_score=z_score
                )
                
                anomalies.append(cost_event)
                
                # Trigger alert
                self.alert_manager.trigger_alert(cost_event)
                
        return anomalies
    
    def set_anomaly_threshold(self, threshold: float):
        """Set the anomaly detection threshold (standard deviations)."""
        self.anomaly_threshold = threshold