/**
 * CostService
 *
 * • Polls a remote cost API at a configurable interval.
 * • Emits 'update' with a CostData instance whenever new data arrives.
 * • Emits 'error' when a fetch or parsing error occurs.
 * • Provides a one‑shot `getLatest()` that returns the most recent data.
 *
 * Configuration (via env or constructor options):
 *   COST_API_URL      – API endpoint (default: https://api.mockcloud.com/v1/costs)
 *   POLL_INTERVAL_MS  – Polling frequency in ms (default: 5 min)
 */

const EventEmitter = require('events');
const fetch = require('node-fetch');
const { CostData } = require('../models/costData');

const DEFAULT_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes

class CostService extends EventEmitter {
  /**
   * @param {Object} [options]
   * @param {string} [options.apiEndpoint]  – override env var
   * @param {number} [options.pollIntervalMs] – override env var
   */
  constructor(options = {}) {
    super();
    this.apiEndpoint =
      options.apiEndpoint || process.env.COST_API_URL || 'https://api.mockcloud.com/v1/costs';
    this.pollIntervalMs =
      options.pollIntervalMs ||
      Number(process.env.POLL_INTERVAL_MS) ||
      DEFAULT_INTERVAL_MS;

    this.timer = null;
    this.latestData = null;
  }

  /** Starts the polling loop (idempotent) */
  start() {
    if (this.timer) return; // already running
    this._fetchAndEmit(); // immediate fetch
    this.timer = setInterval(() => this._fetchAndEmit(), this.pollIntervalMs);
  }

  /** Stops the polling loop */
  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  /** Returns the most recent CostData instance, or null if none yet */
  getLatest() {
    return this.latestData;
  }

  /** Internal: fetches data and emits events */
  async _fetchAndEmit() {
    try {
      const response = await fetch(this.apiEndpoint, {
        headers: { Accept: 'application/json' },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status} ${response.statusText}`);
      }

      const raw = await response.json();
      const data = CostData.fromApiResponse(raw);

      this.latestData = data;
      this.emit('update', data);
    } catch (err) {
      this.emit('error', err);
    }
  }
}

module.exports = { CostService };