import requests
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PrometheusQueryResult:
    metric_name: str
    values: List[float]
    timestamps: List[int]

class PrometheusIntegration:
    def __init__(self, prometheus_url: str, query_timeout: int = 30):
        self.prometheus_url = prometheus_url.rstrip('/')
        self.query_timeout = query_timeout
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def execute_range_query(self, query: str, start_time: int, end_time: int, step: str = '15s') -> PrometheusQueryResult:
        params = {
            'query': query,
            'start': start_time,
            'end': end_time,
            'step': step
        }
        response = self.session.get(
            f"{self.prometheus_url}/api/v1/query_range",
            params=params,
            timeout=self.query_timeout
        )
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'success':
            raise ValueError(f"Prometheus query failed: {data['error']}")
        
        result = data['data']['result']
        if not result:
            return PrometheusQueryResult(metric_name=query, values=[], timestamps=[])
        
        metric_name = result[0]['metric']['__name__']
        values = []
        timestamps = []
        
        for value_set in result[0]['values']:
            timestamps.append(int(value_set[0]))
            values.append(float(value_set[1]))
        
        return PrometheusQueryResult(metric_name=metric_name, values=values, timestamps=timestamps)

    def get_current_metric_value(self, metric_name: str) -> Optional[float]:
        params = {'query': metric_name}
        response = self.session.get(
            f"{self.prometheus_url}/api/v1/query",
            params=params,
            timeout=self.query_timeout
        )
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'success' or not data['data']['result']:
            return None
        
        return float(data['data']['result'][0]['value'][1])

    def get_alerting_rules(self) -> List[Dict]:
        response = self.session.get(
            f"{self.prometheus_url}/api/v1/rules?type=alerting",
            timeout=self.query_timeout
        )
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'success':
            raise ValueError(f"Failed to fetch alerting rules: {data['error']}")
        
        return data['data']['groups']

    def get_metric_labels(self, metric_name: str) -> Dict[str, str]:
        params = {'match[]': metric_name}
        response = self.session.get(
            f"{self.prometheus_url}/api/v1/label/__name__/values",
            params=params,
            timeout=self.query_timeout
        )
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'success':
            raise ValueError(f"Failed to fetch metric labels: {data['error']}")
        
        return data['data']