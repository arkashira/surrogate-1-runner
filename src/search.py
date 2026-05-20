from typing import Dict, List
from tools import get_tools

class Search:
    def __init__(self):
        self.tools = get_tools()

    def search_tools(self, query: str) -> List[Dict]:
        """Search for tools based on a query string."""
        query = query.lower()
        results = []
        for tool in self.tools:
            if (query in tool['name'].lower() or
                query in tool['description'].lower()):
                results.append(tool)
        return results

    def search_features(self, query: str) -> List[Dict]:
        """Search for features based on a query string."""
        query = query.lower()
        results = []
        for tool in self.tools:
            for feature in tool['features']:
                if query in feature.lower():
                    results.append({
                        'tool_name': tool['name'],
                        'feature': feature
                    })
        return results