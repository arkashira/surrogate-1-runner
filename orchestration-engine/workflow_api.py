import json
from typing import List, Dict

class WorkflowDefinition:
    def __init__(self, name: str, tasks: List[Dict]):
        self.name = name
        self.tasks = tasks

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'tasks': self.tasks
        })

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(data['name'], data['tasks'])

class Task:
    def __init__(self, name: str, provider: str, rate_limit: int):
        self.name = name
        self.provider = provider
        self.rate_limit = rate_limit

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'provider': self.provider,
            'rate_limit': self.rate_limit
        })

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(data['name'], data['provider'], data['rate_limit'])

class WorkflowAPI:
    def __init__(self):
        self.workflow_definitions = {}

    def create_workflow(self, name: str, tasks: List[Task]):
        self.workflow_definitions[name] = WorkflowDefinition(name, [task.to_json() for task in tasks])

    def get_workflow(self, name: str):
        return self.workflow_definitions.get(name)

    def save_workflow(self, name: str):
        workflow = self.get_workflow(name)
        if workflow:
            with open(f'{name}.json', 'w') as f:
                f.write(workflow.to_json())

    def load_workflow(self, name: str):
        try:
            with open(f'{name}.json', 'r') as f:
                json_str = f.read()
                return WorkflowDefinition.from_json(json_str)
        except FileNotFoundError:
            return None

# Example usage:
workflow_api = WorkflowAPI()
task1 = Task('task1', 'provider1', 10)
task2 = Task('task2', 'provider2', 20)
workflow_api.create_workflow('my_workflow', [task1, task2])
workflow_api.save_workflow('my_workflow')
loaded_workflow = workflow_api.load_workflow('my_workflow')
print(loaded_workflow.to_json())