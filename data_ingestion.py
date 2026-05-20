"""
Data ingestion module for historical cost data.
"""

import pandas as pd

from models import CostDataPoint

def ingest_cost_data(data_points: List[CostDataPoint]) -> None:
    """Ingest historical cost data for training."""
    # Sort by timestamp
    data_points.sort(key=lambda x: x.timestamp)
    
    # Convert data points to Pandas DataFrame
    df = pd.DataFrame([point.to_dict() for point in data_points])
    
    # Save DataFrame to CSV file
    df.to_csv('historical_data.csv', index=False)