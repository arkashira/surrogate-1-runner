import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ROIService:
    def __init__(self, benchmark_data: Dict, price_data: Dict):
        """
        Initialize ROI service with benchmark and price data
        
        Args:
            benchmark_data: Dictionary mapping component IDs to benchmark metrics
            price_data: Dictionary mapping component IDs to current prices
        """
        self.benchmark_data = benchmark_data
        self.price_data = price_data

    def _validate_benchmark_data(self, benchmark_data: Dict) -> bool:
        """Validate that benchmark data contains required fields"""
        required_fields = ['fps', 'timestamp']
        return all(field in benchmark_data for field in required_fields)

    def _is_recent_benchmark(self, timestamp_str: str, max_age_hours: int = 24) -> bool:
        """Check if benchmark data is recent enough"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return timestamp >= datetime.now() - timedelta(hours=max_age_hours)
        except ValueError:
            logger.warning(f"Invalid timestamp format: {timestamp_str}")
            return False

    def calculate_roi(self, current_rig: Dict, candidate_components: List[Dict]) -> List[Dict]:
        """
        Calculate ROI for candidate components
        
        Args:
            current_rig: Current system configuration
            candidate_components: List of components to evaluate
            
        Returns:
            List of dictionaries containing ROI calculations
        """
        results = []
        
        for component in candidate_components:
            component_id = component.get('id')
            
            # Validate component ID exists in both datasets
            if not component_id or component_id not in self.price_data:
                logger.debug(f"Skipping component {component_id}: missing price data")
                continue
                
            if component_id not in self.benchmark_data:
                logger.debug(f"Skipping component {component_id}: missing benchmark data")
                continue
                
            # Get component data
            benchmark_data = self.benchmark_data[component_id]
            price_usd = self.price_data[component_id]
            
            # Validate benchmark data structure
            if not self._validate_benchmark_data(benchmark_data):
                logger.debug(f"Skipping component {component_id}: invalid benchmark data")
                continue
                
            # Check if benchmark is recent
            timestamp = benchmark_data.get('timestamp')
            if not self._is_recent_benchmark(timestamp):
                logger.debug(f"Skipping component {component_id}: outdated benchmark data")
                continue
                
            # Extract FPS from benchmark data
            fps = benchmark_data.get('fps')
            if not isinstance(fps, (int, float)) or fps <= 0:
                logger.debug(f"Skipping component {component_id}: invalid FPS value")
                continue
                
            # Calculate projected FPS based on upgrade percentage
            upgrade_percentage = component.get('upgrade_percentage', 0)
            if not isinstance(upgrade_percentage, (int, float)):
                logger.debug(f"Skipping component {component_id}: invalid upgrade percentage")
                continue
                
            projected_fps = fps * (1 + (upgrade_percentage / 100))
            
            # Calculate FPS per USD ratio
            if price_usd <= 0:
                logger.debug(f"Skipping component {component_id}: invalid price")
                continue
                
            fps_per_usd = projected_fps / price_usd
            
            # Add result
            results.append({
                'component_id': component_id,
                'projected_fps': round(projected_fps, 2),
                'price_usd': round(price_usd, 2),
                'fps_per_usd': round(fps_per_usd, 4),
                'upgrade_percentage': upgrade_percentage
            })
            
        return results

    def get_roi(self, current_rig: Dict, candidate_components: List[Dict]) -> Dict:
        """
        Main entry point for ROI calculation
        
        Args:
            current_rig: Current system configuration
            candidate_components: List of components to evaluate
            
        Returns:
            Dictionary containing ROI results
        """
        results = self.calculate_roi(current_rig, candidate_components)
        return {
            'results': results,
            'total_components_evaluated': len(candidate_components),
            'components_with_roi': len(results),
            'timestamp': datetime.now().isoformat()
        }

def create_roi_service(benchmark_data: Dict, price_data: Dict) -> ROIService:
    """Factory function to create ROI service instance"""
    return ROIService(benchmark_data, price_data)