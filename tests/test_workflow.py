import unittest
from surrogate_1.core.workflow import WorkflowInstance, Agent, Interaction

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow_instance = WorkflowInstance()
        self.agent1 = Agent(id=1, name="Agent1")
        self.agent2 = Agent(id=2, name="Agent2")
        self.interaction = Interaction(type="message", target_agent_id=2)
        self.agent1.interactions.append(self.interaction)
        self.workflow_instance.agents.extend([self.agent1, self.agent2])

    def test_agent_creation(self):
        self.assertEqual(self.agent1.id, 1)
        self.assertEqual(self.agent1.name, "Agent1")
        self.assertEqual(len(self.agent1.interactions), 1)

    def test_workflow_instance(self):
        self.assertEqual(len(self.workflow_instance.agents), 2)

if __name__ == '__main__':
    unittest.main()