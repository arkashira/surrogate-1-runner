import logging

class BuildRecommendation:
    def __init__(self, budget, preferences):
        self.budget = budget
        self.preferences = preferences

    def get_compatible_components(self):
        # For simplicity, assume we have a list of components
        components = [
            {"name": "CPU", "price": 100},
            {"name": "GPU", "price": 200},
            {"name": "RAM", "price": 50},
            # Add more components here
        ]

        compatible_components = []
        for component in components:
            if component["price"] <= self.budget:
                compatible_components.append(component)

        return compatible_components

    def adjust_recommendations(self, specific_needs):
        # For simplicity, assume we have a list of specific needs
        specific_needs_list = [
            {"name": "High-performance GPU", "price": 300},
            {"name": "High-capacity RAM", "price": 100},
            # Add more specific needs here
        ]

        adjusted_components = []
        for component in self.get_compatible_components():
            if specific_needs["name"] in specific_needs_list:
                adjusted_components.append(component)

        return adjusted_components

# Example usage:
budget = 500
preferences = {"CPU": "Intel", "GPU": "NVIDIA"}
specific_needs = {"name": "High-performance GPU"}

build_recommendation = BuildRecommendation(budget, preferences)
compatible_components = build_recommendation.get_compatible_components()
adjusted_components = build_recommendation.adjust_recommendations(specific_needs)

print("Compatible components:", compatible_components)
print("Adjusted components:", adjusted_components)