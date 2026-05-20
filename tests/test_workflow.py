import unittest
from src.workflow import WorkflowDefinition, WorkflowInstance, LLMAgentConfig

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.agent_configs = [
            LLMAgentConfig(
                agent_id="agent1",
                model_name="model1",
                api_key="key1",
                parameters={"param1": "value1"}
            ),
            LLMAgentConfig(
                agent_id="agent2",
                model_name="model2",
                api_key="key2",
                parameters={"param2": "value2"}
            )
        ]
        self.workflow_definition = WorkflowDefinition(
            workflow_id="test_workflow",
            agents=self.agent_configs,
            connections={"agent1": ["agent2"]}
        )
        self.workflow_instance = WorkflowInstance(self.workflow_definition)

    def test_validate(self):
        self.assertTrue(self.workflow_instance.validate())

    def test_create_instance(self):
        self.workflow_instance.create_instance()

    def test_execute(self):
        input_data = {"agent1": "prompt1", "agent2": "prompt2"}
        results = self.workflow_instance.execute(input_data)
        self.assertEqual(results["agent1"], "Response from agent1")
        self.assertEqual(results["agent2"], "Response from agent2")

    def test_cleanup(self):
        self.workflow_instance.cleanup()

if __name__ == '__main__':
    unittest.main()