export interface PersistedEvent {
  event: string;
  properties: Record<string, unknown>;
}

/**
 * Browser: localStorage (synchronous, simple)
 * Node: JSON file under OS temp dir (fallback for SSR/CLI)
 */
export class EventStore {
  private static readonly KEY = 'pending_analytics_events';
  private static readonly FILE = `${process.cwd()}/.analytics-pending.json`;

  static getAll(): PersistedEvent[] {
    if (typeof window !== 'undefined') {
      try {
        return JSON.parse(localStorage.getItem(this.KEY) ?? '[]');
      } catch {
        return [];
      }
    }
    // Node path
    try {
      const raw = require('fs').readFileSync(this.FILE, 'utf-8');
      return JSON.parse(raw);
    } catch {
      return [];
    }
  }

  static setAll(events: PersistedEvent[]) {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.KEY, JSON.stringify(events));
    } else {
      const fs = require('fs');
      fs.writeFileSync(this.FILE, JSON.stringify(events, null, 2));
    }
  }

  static push(event: PersistedEvent) {
    const all = this.getAll();
    all.push(event);
    this.setAll(all);
  }

  static clear() {
    this.setAll([]);
  }
}