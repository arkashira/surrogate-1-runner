import { Visualization, VisualizationConfig } from './visualization';
import { InteractionBus, AgentInteraction } from './agent_interaction';

// Configuration
const config: VisualizationConfig = {
  width: 800,
  height: 600,
  container: '#visualization-container' // Optional custom container
};

// Initialize visualization
const visualization = new Visualization(config);

// Get the interaction bus instance
const bus = InteractionBus.getInstance();

// Simulate periodic interactions
setInterval(() => {
  const interactions: AgentInteraction[] = [
    {
      id: '1',
      x: 100 + Math.random() * 100,
      y: 100 + Math.random() * 100,
      timestamp: Date.now(),
      from: 'agent1',
      to: 'agent2',
      description: 'Movement interaction'
    },
    {
      id: '2',
      x: 200 + Math.random() * 100,
      y: 200 + Math.random() * 100,
      timestamp: Date.now(),
      from: 'agent2',
      to: 'agent1',
      description: 'Response interaction'
    }
  ];

  // Record each interaction
  interactions.forEach(interaction => bus.record(interaction));
}, 1000);