from .compatibility import CompatibilityRules
from .component import CPU, Motherboard, GPU, PSU, Case

class Engine:
    def __init__(self):
        self.compatibility_rules = CompatibilityRules()
        self.components = {
            "cpu": [],
            "motherboard": [],
            "gpu": [],
            "psu": [],
            "case": [],
        }

    def add_component(self, component):
        self.components[component.name].append(component)

    def suggest_build(self, budget, use_case):
        suggested_build = {}
        for component_type in self.components:
            for component in self.components[component_type]:
                if component.price <= budget * 1.05 and component.price >= budget * 0.95:
                    suggested_build[component_type] = component
        if self.compatibility_rules.check_compatibility(suggested_build):
            return suggested_build
        else:
            # find closest higher-budget alternative
            closest_alternative = None
            closest_alternative_price = float("inf")
            for component_type in self.components:
                for component in self.components[component_type]:
                    if component.price > budget and component.price < closest_alternative_price:
                        closest_alternative = component
                        closest_alternative_price = component.price
            return {"warning": "No exact fit exists, suggesting closest higher-budget alternative", "build": closest_alternative}