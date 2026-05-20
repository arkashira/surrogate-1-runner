from typing import Dict, List

def get_tools() -> List[Dict]:
    """Return a list of tools with their features and descriptions."""
    return [
        {
            'name': 'Data Ingestion',
            'description': 'Tools for ingesting and processing data',
            'features': ['streaming', 'normalization', 'deduplication']
        },
        {
            'name': 'Data Analysis',
            'description': 'Tools for analyzing and visualizing data',
            'features': ['statistics', 'visualization', 'reporting']
        },
        {
            'name': 'Data Storage',
            'description': 'Tools for storing and managing data',
            'features': ['database', 'backup', 'recovery']
        }
    ]