import argparse
import yaml
import time
import fnmatch
from pathlib import Path
from typing import Dict, List, Optional

class FilterConfig:
    def __init__(self, config_path: str = "config/filter_config.yaml"):
        self.config_path = config_path
        self._config = None
        self._load_config()
    
    def _load_config(self):
        """Lazy load configuration to handle missing files gracefully."""
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except FileNotFoundError:
            self._config = {'filter_settings': {'enabled': False}}
    
    @property
    def enabled(self) -> bool:
        return self._config.get('filter_settings', {}).get('enabled', False)
    
    @property
    def threshold(self) -> float:
        return self._config.get('filter_settings', {}).get('threshold', 0.05)
    
    @property
    def max_duration_seconds(self) -> int:
        return self._config.get('filter_settings', {}).get('max_duration_seconds', 2)
    
    @property
    def component_mapping(self) -> Dict[str, List[str]]:
        return self._config.get('filter_settings', {}).get('component_mapping', {})

    def _matches_pattern(self, component: str, patterns: List[str]) -> bool:
        """Check if component matches any of the given patterns."""
        for pattern in patterns:
            # Convert glob pattern to fnmatch
            if fnmatch.fnmatch(component, pattern) or fnmatch.fnmatch(component, pattern.replace('**', '*')):
                return True
        return False

    def get_relevant_tests(self, changed_components: List[str]) -> List[str]:
        """
        Determine which tests are relevant based on changed components.
        
        Args:
            changed_components: List of file paths that have changed
            
        Returns:
            List of test file paths that should be run
        """
        if not self.enabled:
            return []
        
        start_time = time.time()
        relevant_tests = set()
        
        # Map changed components to their category and find relevant tests
        for component in changed_components:
            # Check infrastructure changes
            if self._matches_pattern(component, self.component_mapping.get('infrastructure', [])):
                relevant_tests.add('tests/infrastructure/')
            
            # Check application changes  
            if self._matches_pattern(component, self.component_mapping.get('application', [])):
                relevant_tests.add('tests/application/')
            
            # Check if tests themselves changed
            if self._matches_pattern(component, self.component_mapping.get('tests', [])):
                relevant_tests.add('tests/')
        
        # Check timeout
        elapsed = time.time() - start_time
        if elapsed > self.max_duration_seconds:
            raise TimeoutError(f"Filtering exceeded maximum duration of {self.max_duration_seconds} seconds (took {elapsed:.2f}s)")
        
        return sorted(relevant_tests)


def main():
    parser = argparse.ArgumentParser(description='Filter test paths based on changed components.')
    parser.add_argument('--changed-components', nargs='+', help='List of changed components')
    parser.add_argument('--config', default='config/filter_config.yaml', help='Path to config file')
    args = parser.parse_args()

    config = FilterConfig(args.config)
    
    if not config.enabled:
        print("Filtering is disabled. Running all tests.")
        return
    
    relevant_tests = config.get_relevant_tests(args.changed_components or [])
    
    print("Relevant test paths:")
    for test in relevant_tests:
        print(test)


if __name__ == "__main__":
    main()