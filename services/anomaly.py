import os
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from ..config import COSTINEL_API_KEY, COSTINEL_BASE_URL
from ..utils import logger

def get_costinel_resource_breakdown(
    alert_id: str,
    time_range: str = "last_hour"
) -> List[Dict]:
    """
    Fetch resource breakdown from Costinel API for a specific alert
    Returns top 5 resources with cost, percentage, and links
    """
    try:
        # Calculate time range parameters
        end_time = datetime.utcnow().isoformat() + "Z"
        if time_range == "last_hour":
            start_time = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"
        else:  # default to last day
            start_time = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"

        # Build API request
        headers = {
            "Authorization": f"Bearer {COSTINEL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "alert_id": alert_id,
            "start_time": start_time,
            "end_time": end_time,
            "limit": 5
        }

        response = requests.get(
            f"{COSTINEL_BASE_URL}/api/v1/anomalies/resources",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"Costinel API error: {response.status_code} - {response.text}")
            raise CostinelAPIError(f"API request failed: {response.status_code}")

        data = response.json()
        total_cost = sum(item["cost"] for item in data)
        
        # Format results with percentages and links
        return [
            {
                "resource_id": item["resource_id"],
                "resource_type": item["resource_type"],
                "cost": round(item["cost"], 2),
                "percentage": round((item["cost"] / total_cost) * 100, 1) if total_cost > 0 else 0,
                "link": f"{COSTINEL_BASE_URL}/resources/{item['resource_id']}/details"
            }
            for item in sorted(data, key=lambda x: x["cost"], reverse=True)[:5]
        ]
        
    except requests.exceptions.RequestException as e:
        logger.exception("Costinel API request failed")
        raise CostinelAPIError(f"Network error: {str(e)}") from e

class CostinelAPIError(Exception):
    """Custom exception for Costinel API errors"""
    pass