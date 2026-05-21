from typing import List, Dict

class ApprovedModel:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

class ModelRegistry:
    def __init__(self):
        self.approved_models: List[ApprovedModel] = []

    def add_approved_model(self, model: ApprovedModel):
        self.approved_models.append(model)

    def get_approved_models(self) -> List[ApprovedModel]:
        return self.approved_models

# src/models.py