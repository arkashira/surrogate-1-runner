import numpy as np
from typing import Dict, List

class FPSCalculator:
    def __init__(self, base_fps: float):
        self.base_fps = base_fps
        self.component_performance_data = {}

    def add_component_performance_data(self, component_name: str, performance_data: Dict[str, float]):
        self.component_performance_data[component_name] = performance_data

    def calculate_fps_gain(self, component_name: str, upgrade_level: int) -> float:
        if component_name not in self.component_performance_data:
            raise ValueError(f"No performance data for component: {component_name}")

        performance_data = self.component_performance_data[component_name]
        if upgrade_level not in performance_data:
            raise ValueError(f"No performance data for upgrade level: {upgrade_level}")

        fps_gain = performance_data[upgrade_level] - self.base_fps
        return fps_gain

    def calculate_fps_gain_per_dollar(self, component_name: str, upgrade_level: int, cost: float) -> float:
        fps_gain = self.calculate_fps_gain(component_name, upgrade_level)
        return fps_gain / cost

    def get_sorted_components_by_fps_gain_per_dollar(self, upgrade_level: int, costs: Dict[str, float]) -> List[Dict[str, float]]:
        components = []
        for component_name in self.component_performance_data:
            fps_gain_per_dollar = self.calculate_fps_gain_per_dollar(component_name, upgrade_level, costs[component_name])
            components.append({
                'component_name': component_name,
                'fps_gain_per_dollar': fps_gain_per_dollar
            })

        sorted_components = sorted(components, key=lambda x: x['fps_gain_per_dollar'], reverse=True)
        return sorted_components