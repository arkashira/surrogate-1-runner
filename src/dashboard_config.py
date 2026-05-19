import os
from typing import List, Dict

def get_connected_repositories() -> List[Dict]:
    """Fetch connected repositories from configuration store"""
    # In production, this would query a database or auth service
    return [
        {
            'name': 'axentx/surrogate-1',
            'owner': 'axentx',
            'url': 'https://github.com/axentx/surrogate-1',
            'connected_at': '2026-05-04T14:30:00Z'
        },
        {
            'name': 'axentx/core',
            'owner': 'axentx',
            'url': 'https://github.com/axentx/core',
            'connected_at': '2026-05-03T09:15:00Z'
        }
    ]