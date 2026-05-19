import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

interface Event {
  type: string;
  timestamp: number;
  userId: string;
  metadata?: Record<string, unknown>; // Added for extensibility
}

class Telemetry {
  private events: Event[] = [];
  private userId: string;
  private readonly endpoint: string;
  private readonly sendInterval: number;

  constructor({
    endpoint = 'https://api.example.com/telemetry',
    sendInterval = 24 * 60 * 60 * 1000 // Default: daily
  } = {}) {
    this.userId = localStorage.getItem('telemetryUserId') || uuidv4();
    localStorage.setItem('telemetryUserId', this.userId);
    this.endpoint = endpoint;
    this.sendInterval = sendInterval;
  }

  private trackEvent(type: string, metadata?: Record<string, unknown>) {
    const event: Event = {
      type,
      timestamp: Date.now(),
      userId: this.userId,
      metadata
    };
    this.events.push(event);
  }

  private async sendEvents() {
    if (this.events.length === 0) return;

    try {
      await axios.post(this.endpoint, this.events);
      this.events = [];
    } catch (error) {
      console.error('Telemetry error:', error);
      // Implement retry logic or queue for later
    }
  }

  start() {
    this.trackEvent('session_start');
    setInterval(() => this.sendEvents(), this.sendInterval);

    // Add beforeunload handler for final event send
    window.addEventListener('beforeunload', () => this.sendEvents());
  }

  // Specific event methods with optional metadata
  suggestionRequested(metadata?: Record<string, unknown>) {
    this.trackEvent('suggestion_requested', metadata);
  }

  suggestionAccepted(metadata?: Record<string, unknown>) {
    this.trackEvent('suggestion_accepted', metadata);
  }

  suggestionRejected(metadata?: Record<string, unknown>) {
    this.trackEvent('suggestion_rejected', metadata);
  }

  // Add more event methods as needed
}

// Singleton pattern for easy access
const telemetry = new Telemetry();
export default telemetry;