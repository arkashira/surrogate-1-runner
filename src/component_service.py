from expert_insights import ExpertInsights

class ComponentService:
    def __init__(self, api_key):
        self.expert_insights = ExpertInsights(api_key)

    def get_component_insights(self, component_id):
        return self.expert_insights.get_validated_insights(component_id)