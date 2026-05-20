import unittest
from src.services.workflow_registry import WorkflowRegistry

class TestWorkflowRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = WorkflowRegistry("test_registry.json")

    def tearDown(self):
        self.registry.file_path.unlink()

    def test_add_workflow(self):
        workflow_id = "test-workflow"
        steps = {"step1": "do something", "step2": "do something else"}
        self.registry.add_workflow(workflow_id, steps)
        self.assertEqual(self.registry.get_workflow(workflow_id), steps)

    def test_add_existing_workflow(self):
        workflow_id = "test-workflow"
        steps = {"step1": "do something", "step2": "do something else"}
        self.registry.add_workflow(workflow_id, steps)
        with self.assertRaises(ValueError):
            self.registry.add_workflow(workflow_id, {"step3": "do something new"})

    def test_get_nonexistent_workflow(self):
        self.assertIsNone(self.registry.get_workflow("nonexistent_id"))

    def test_list_workflows(self):
        workflow_id1 = "test-workflow-1"
        steps1 = {"step1": "do something"}
        self.registry.add_workflow(workflow_id1, steps1)

        workflow_id2 = "test-workflow-2"
        steps2 = {"step2": "do something else"}
        self.registry.add_workflow(workflow_id2, steps2)

        workflows = self.registry.list_workflows()
        self.assertEqual(len(workflows), 2)
        self.assertIn(workflow_id1, workflows)
        self.assertIn(workflow_id2, workflows)

    def test_save_load_registry(self):
        workflow_id = "test-workflow"
        steps = {"step1": "do something", "step2": "do something else"}
        self.registry.add_workflow(workflow_id, steps)

        loaded_registry = WorkflowRegistry("test_registry.json")
        self.assertEqual(loaded_registry.get_workflow(workflow_id), steps)

if __name__ == "__main__":
    unittest.main()