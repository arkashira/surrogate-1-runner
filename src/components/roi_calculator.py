from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Component:
    name: str
    component_type: str
    price: float
    fps_gain: float

class ROICalculator:
    def __init__(self, components: List[Component]):
        self.components = components

    def calculate_roi(self) -> List[Dict]:
        roi_list = []
        for component in self.components:
            roi = component.fps_gain / component.price
            roi_list.append({
                'name': component.name,
                'component_type': component.component_type,
                'price': component.price,
                'fps_gain': component.fps_gain,
                'roi': roi
            })
        return sorted(roi_list, key=lambda x: x['roi'], reverse=True)

    def filter_by_type(self, component_type: str) -> List[Dict]:
        filtered_components = [comp for comp in self.components if comp.component_type == component_type]
        return self.calculate_roi(filtered_components)