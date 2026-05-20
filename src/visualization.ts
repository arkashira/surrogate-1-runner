import * as d3 from 'd3';
import { AgentInteraction, InteractionBus } from './agent_interaction';

interface VisualizationConfig {
  width: number;
  height: number;
  container?: string; // Optional container selector
}

class Visualization {
  private svg: any;
  private config: VisualizationConfig;
  private interactionBus: InteractionBus;

  constructor(config: VisualizationConfig) {
    this.config = config;
    this.interactionBus = InteractionBus.getInstance();

    // Create SVG container
    const container = config.container || 'body';
    this.svg = d3.select(container)
      .append('svg')
      .attr('width', config.width)
      .attr('height', config.height);

    // Set up event listener
    this.interactionBus.onInteraction((interaction: AgentInteraction) => {
      this.update([interaction]);
    });
  }

  public update(interactions: AgentInteraction[]): void {
    // Update existing circles
    const circles = this.svg.selectAll('circle')
      .data(interactions, (d: AgentInteraction) => d.id);

    // Enter new circles
    circles.enter()
      .append('circle')
      .attr('cx', (d: AgentInteraction) => d.x)
      .attr('cy', (d: AgentInteraction) => d.y)
      .attr('r', 10)
      .attr('fill', 'steelblue');

    // Update existing circles
    circles
      .attr('cx', (d: AgentInteraction) => d.x)
      .attr('cy', (d: AgentInteraction) => d.y);

    // Remove old circles
    circles.exit().remove();
  }
}

export { Visualization, VisualizationConfig };