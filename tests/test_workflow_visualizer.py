import unittest
from surrogate_1.core.workflow import WorkflowInstance, Agent, Interaction
from surrogate_1.src.workflow_visualizer import WorkflowVisualizer

class TestWorkflowVisualizer(unittest.TestCase):
    def setUp(self):
        self.workflow_instance = WorkflowInstance()
        self.agent1 = Agent(id=1, name="Agent1")
        self.agent2 = Agent(id=2, name="Agent2")
        self.interaction = Interaction(type="message", target_agent_id=2)
        self.agent1.interactions.append(self.interaction)
        self.workflow_instance.agents.extend([self.agent1, self.agent2])
        self.visualizer = WorkflowVisualizer(self.workflow_instance)

    def test_build_graph(self):
        self.visualizer.build_graph()
        self.assertEqual(len(self.visualizer.graph.nodes), 2)
        self.assertEqual(len(self.visualizer.graph.edges), 1)

    def test_update_graph(self):
        self.visualizer.build_graph()
        self.visualizer.update_graph()
        self.assertEqual(len(self.visualizer.graph.nodes), 2)
        self.assertEqual(len(self.visualizer.graph.edges), 1)

if __name__ == '__main__':
    unittest.main()