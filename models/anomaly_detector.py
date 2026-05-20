import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CostAnomaly:
    timestamp: datetime
    service: str
    severity: str  # 'LOW' or 'HIGH'
    current_spend: float
    rolling_avg: float
    multiplier: float

class AnomalyDetector:
    """Detects cost anomalies using rolling 7-day average."""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.anomalies: List[CostAnomaly] = []
    
    def detect_anomalies(self, cost_data: List[Dict[str, Any]]) -> List[CostAnomaly]:
        """
        Detect anomalies where spend exceeds 3× the rolling 7-day average.
        
        Args:
            cost_data: List of cost records with keys:
                - timestamp: datetime
                - service: str
                - spend: float
        
        Returns:
            List of detected CostAnomaly objects
        """
        self.anomalies = []
        
        # Group data by service
        by_service: Dict[str, List[Dict[str, Any]]] = {}
        for record in cost_data:
            service = record['service']
            if service not in by_service:
                by_service[service] = []
            by_service[service].append(record)
        
        # Process each service
        for service, records in by_service.items():
            # Sort by timestamp
            records.sort(key=lambda x: x['timestamp'])
            
            # Calculate rolling 7-day average and detect anomalies
            for i, record in enumerate(records):
                current_spend = record['spend']
                current_ts = record['timestamp']
                
                # Get last 7 days of data (excluding current)
                window_start = current_ts - timedelta(days=7)
                window_data = [
                    r for r in records[:i]
                    if r['timestamp'] >= window_start
                ]
                
                if len(window_data) < 3:
                    continue  # Not enough data for meaningful average
                
                rolling_avg = statistics.mean([r['spend'] for r in window_data])
                
                if rolling_avg == 0:
                    continue  # Avoid division by zero
                
                multiplier = current_spend / rolling_avg
                
                if multiplier > 2.0:  # Threshold for anomaly
                    if multiplier > 3.0:
                        severity = 'HIGH'
                    else:
                        severity = 'LOW'
                    
                    anomaly = CostAnomaly(
                        timestamp=current_ts,
                        service=service,
                        severity=severity,
                        current_spend=current_spend,
                        rolling_avg=rolling_avg,
                        multiplier=multiplier
                    )
                    self.anomalies.append(anomaly)
        
        return self.anomalies
    
    def store_anomalies(self) -> int:
        """
        Store detected anomalies in the cost_anomalies table.
        
        Returns:
            Number of anomalies stored
        """
        cursor = self.db.cursor()
        count = 0
        
        for anomaly in self.anomalies:
            try:
                cursor.execute("""
                    INSERT INTO cost_anomalies 
                    (timestamp, service, severity, current_spend, rolling_avg, multiplier)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    anomaly.timestamp,
                    anomaly.service,
                    anomaly.severity,
                    anomaly.current_spend,
                    anomaly.rolling_avg,
                    anomaly.multiplier
                ))
                count += 1
            except Exception as e:
                logger.error(f"Failed to store anomaly: {e}")
        
        self.db.commit()
        return count
    
    def get_anomalies(self, service: Optional[str] = None, 
                      severity: Optional[str] = None) -> List[CostAnomaly]:
        """
        Retrieve anomalies from the database.
        
        Args:
            service: Filter by service name (optional)
            severity: Filter by severity level (optional)
        
        Returns:
            List of CostAnomaly objects
        """
        cursor = self.db.cursor()
        
        query = "SELECT * FROM cost_anomalies WHERE 1=1"
        params = []
        
        if service:
            query += " AND service = %s"
            params.append(service)
        
        if severity:
            query += " AND severity = %s"
            params.append(severity)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        anomalies = []
        for row in rows:
            anomaly = CostAnomaly(
                timestamp=row['timestamp'],
                service=row['service'],
                severity=row['severity'],
                current_spend=row['current_spend'],
                rolling_avg=row['rolling_avg'],
                multiplier=row['multiplier']
            )
            anomalies.append(anomaly)
        
        return anomalies

# Module exports
__all__ = ['AnomalyDetector', 'CostAnomaly']