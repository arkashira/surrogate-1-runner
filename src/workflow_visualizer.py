import networkx as nx
import matplotlib.pyplot as plt
from surrogate_1.core.workflow import WorkflowInstance

class WorkflowVisualizer:
    def __init__(self, workflow_instance: WorkflowInstance):
        self.workflow_instance = workflow_instance
        self.graph = nx.DiGraph()

    def build_graph(self):
        for agent in self.workflow_instance.agents:
            self.graph.add_node(agent.id, label=agent.name)
            for interaction in agent.interactions:
                self.graph.add_edge(agent.id, interaction.target_agent_id, label=interaction.type)

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, labels=nx.get_node_attributes(self.graph, 'label'))
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()

    def update_graph(self):
        self.graph.clear()
        self.build_graph()
        self.draw_graph()