import unittest
from workflow_api import WorkflowAPI, Task, WorkflowDefinition

class TestWorkflowAPI(unittest.TestCase):
    def test_create_workflow(self):
        workflow_api = WorkflowAPI()
        task1 = Task('task1', 'provider1', 10)
        task2 = Task('task2', 'provider2', 20)
        workflow_api.create_workflow('my_workflow', [task1, task2])
        self.assertIn('my_workflow', workflow_api.workflow_definitions)

    def test_get_workflow(self):
        workflow_api = WorkflowAPI()
        task1 = Task('task1', 'provider1', 10)
        task2 = Task('task2', 'provider2', 20)
        workflow_api.create_workflow('my_workflow', [task1, task2])
        workflow = workflow_api.get_workflow('my_workflow')
        self.assertIsNotNone(workflow)

    def test_save_workflow(self):
        workflow_api = WorkflowAPI()
        task1 = Task('task1', 'provider1', 10)
        task2 = Task('task2', 'provider2', 20)
        workflow_api.create_workflow('my_workflow', [task1, task2])
        workflow_api.save_workflow('my_workflow')
        with open('my_workflow.json', 'r') as f:
            json_str = f.read()
            self.assertIsNotNone(json_str)

    def test_load_workflow(self):
        workflow_api = WorkflowAPI()
        task1 = Task('task1', 'provider1', 10)
        task2 = Task('task2', 'provider2', 20)
        workflow_api.create_workflow('my_workflow', [task1, task2])
        workflow_api.save_workflow('my_workflow')
        loaded_workflow = workflow_api.load_workflow('my_workflow')
        self.assertIsNotNone(loaded_workflow)

if __name__ == '__main__':
    unittest.main()