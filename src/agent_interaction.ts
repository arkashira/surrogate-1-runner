import { EventEmitter } from 'events';

/**
 * Represents an agent interaction with position data
 */
export interface AgentInteraction {
  id: string;
  x: number;
  y: number;
  timestamp: number;
  from?: string;       // Optional source agent
  to?: string;         // Optional target agent
  description?: string; // Optional description
  payload?: Record<string, unknown>; // Optional payload
}

/**
 * Singleton event bus for managing interaction events
 */
export class InteractionBus extends EventEmitter {
  private static instance: InteractionBus;

  private constructor() {
    super();
  }

  public static getInstance(): InteractionBus {
    if (!InteractionBus.instance) {
      InteractionBus.instance = new InteractionBus();
    }
    return InteractionBus.instance;
  }

  public record(interaction: AgentInteraction): void {
    this.emit('interaction', interaction);
  }

  public onInteraction(listener: (interaction: AgentInteraction) => void): void {
    this.on('interaction', listener);
  }
}