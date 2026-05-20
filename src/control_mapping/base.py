from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class Control:
    """Represents a single control requirement."""
    control_id: str
    description: str
    requirements: List[str]
    category: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'control_id': self.control_id,
            'description': self.description,
            'requirements': self.requirements,
            'category': self.category
        }


class BaseControlMapper(ABC):
    """Abstract base class for control mapping frameworks."""
    
    def __init__(self):
        self.control_mapping: Dict[str, Dict[str, Control]] = {}
        self._initialize_controls()
    
    @abstractmethod
    def _initialize_controls(self) -> None:
        """Initialize the control framework. Must be implemented by subclasses."""
        pass
    
    def map_controls(self, infrastructure_components: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Map infrastructure components to applicable controls."""
        mapped_controls = {}
        
        for component, details in infrastructure_components.items():
            mapped_controls[component] = []
            
            # Handle both string categories and dict with 'category' key
            component_categories = self._extract_categories(details)
            
            for category in component_categories:
                if category in self.control_mapping:
                    for control_id, control in self.control_mapping[category].items():
                        mapped_controls[component].append(control.to_dict())
        
        return mapped_controls
    
    def _extract_categories(self, details: Any) -> List[str]:
        """Extract category names from component details."""
        if isinstance(details, dict):
            if 'category' in details:
                return [details['category']]
            return [k for k, v in details.items() if v]
        elif isinstance(details, str):
            return [details]
        return []
    
    def validate_controls(self, mapped_controls: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        """Validate that all required controls are mapped."""
        validation_results = {}
        
        for component, controls in mapped_controls.items():
            mapped_control_ids = {c['control_id'] for c in controls}
            mapped_categories = set()
            
            for ctrl in controls:
                # Extract category from control_id prefix (e.g., "PDPA" from "PDPA-1")
                prefix = ctrl['control_id'].split('-')[0]
                mapped_categories.add(prefix.lower())
            
            # Find missing controls
            missing_controls = []
            for category, controls_dict in self.control_mapping.items():
                for ctrl_id, ctrl in controls_dict.items():
                    if ctrl_id not in mapped_control_ids:
                        missing_controls.append({
                            'control_id': ctrl_id,
                            'category': category,
                            'description': ctrl.description
                        })
            
            validation_results[component] = {
                'covered_controls': controls,
                'covered_control_ids': list(mapped_control_ids),
                'missing_controls': missing_controls,
                'coverage_percentage': (
                    len(mapped_control_ids) / 
                    sum(len(cats) for cats in self.control_mapping.values()) * 100
                    if self.control_mapping else 0
                )
            }
        
        return validation_results
    
    def get_control_by_id(self, control_id: str) -> Control | None:
        """Retrieve a specific control by its ID."""
        for category_controls in self.control_mapping.values():
            if control_id in category_controls:
                return category_controls[control_id]
        return None
    
    def get_controls_by_category(self, category: str) -> List[Control]:
        """Get all controls for a specific category."""
        return list(self.control_mapping.get(category, {}).values())