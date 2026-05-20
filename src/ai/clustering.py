import re
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from datetime import datetime

def extract_service(alert: Dict[str, Any]) -> str:
    """Extract service/namespace from alert metadata"""
    # Try multiple patterns to identify service
    service_patterns = [
        r'services/(.+?)/',  # GCP-style
        r'namespace:(.+)/',  # Kubernetes
        r'application-(.+)_' # AWS
    ]
    
    for pattern in service_patterns:
        match = re.search(pattern, alert.get('resource', ''))
        if match:
            return match.group(1).lower()
    
    # Fallback to direct field
    return alert.get('service', 'unknown')

def cluster_alerts(alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Group alerts by service and consolidate with suppression tracking"""
    service_clusters = defaultdict(lambda: {
        'alerts': [],
        'suppressed_count': 0
    })
    
    # Group by service and sort by recency
    for alert in alerts:
        service = extract_service(alert)
        alert['timestamp'] = datetime.fromisoformat(alert['timestamp'])
        service_clusters[service]['alerts'].append(alert)
    
    # Process each cluster
    result = []
    for service, cluster in service_clusters.items():
        # Sort by most recent first
        sorted_alerts = sorted(
            cluster['alerts'], 
            key=lambda x: x['timestamp'], 
            reverse=True
        )
        
        # Take top 3-5 alerts (configurable threshold)
        SHOW_LIMIT = 4
        shown = sorted_alerts[:SHOW_LIMIT]
        suppressed = len(sorted_alerts) - SHOW_LIMIT
        
        result.append({
            'service': service,
            'alerts': [{
                'id': a['id'],
                'message': a['message'],
                'timestamp': a['timestamp'].isoformat(),
                'severity': a['severity']
            } for a in shown],
            'suppressed_count': max(0, suppressed),
            'total_alerts': len(cluster['alerts'])
        })
    
    # Sort clusters by most active first
    return sorted(result, key=lambda x: x['total_alerts'], reverse=True)