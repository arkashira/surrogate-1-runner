import { makeAutoObservable, runInAction } from 'mobx';

const STORAGE_KEY = 'alertConfig';

class AlertStore {
  // 1️⃣  Default values – will be overwritten by persisted data
  threshold = 1000;          // spending threshold in dollars
  email = '';                // e‑mail address
  slackWebhook = '';         // Slack webhook URL

  // 2️⃣  Listeners for non‑React code
  listeners = new Set();

  constructor() {
    // 3️⃣  Make all fields observable & actions
    makeAutoObservable(this, {}, { autoBind: true });

    // 4️⃣  Load persisted config
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        runInAction(() => {
          this.threshold = parsed.threshold ?? this.threshold;
          this.email = parsed.email ?? this.email;
          this.slackWebhook = parsed.slackWebhook ?? this.slackWebhook;
        });
      } catch (_) {
        // ignore malformed JSON
      }
    }
  }

  /* -----------------  Persistence helpers  ----------------- */

  /** Persist current state to localStorage */
  persist() {
    const payload = {
      threshold: this.threshold,
      email: this.email,
      slackWebhook: this.slackWebhook,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  }

  /* -----------------  Observable actions  ----------------- */

  setThreshold(v) {
    this.threshold = Number(v);
    this.persist();
    this.notify();
  }

  setEmail(v) {
    this.email = v;
    this.persist();
    this.notify();
  }

  setSlackWebhook(v) {
    this.slackWebhook = v;
    this.persist();
    this.notify();
  }

  /* -----------------  Subscription API  ----------------- */

  /** Subscribe a callback that receives the current config */
  subscribe(fn) {
    this.listeners.add(fn);
    // immediately fire the callback so the subscriber has the latest state
    fn(this.getConfig());
    return () => this.listeners.delete(fn);
  }

  /** Notify all listeners of the new config */
  notify() {
    const cfg = this.getConfig();
    this.listeners.forEach((fn) => fn(cfg));
  }

  /** Return a plain‑object snapshot of the config */
  getConfig() {
    return {
      threshold: this.threshold,
      email: this.email,
      slackWebhook: this.slackWebhook,
    };
  }
}

export const alertStore = new AlertStore();