/**
 * Marketing Effectiveness Tracking Module
 *
 * Keeps an in‑memory store of metrics, strategy changes and user feedback.
 * Designed for quick prototyping, unit‑testing and nightly clean‑ups.
 * In production you can swap the Map for Redis, a DB, or an analytics SDK.
 *
 * Usage
 *   const tracker = require('./marketing_effectiveness');
 *
 *   tracker.record('ad-123', { impressions: 1000, clicks: 50, conversions: 5 });
 *   console.log(tracker.getEffectiveness('ad-123')); // { total, avg, raw }
 *   tracker.adjustStrategy('ad-123', { budget: 500, target: 'retargeting' });
 *   tracker.submitFeedback({ userId: 'u1', rating: 4, comment: 'Nice tracker' });
 */

const { performance } = require('perf_hooks');

class MarketingEffectivenessTracker {
  constructor() {
    // { tacticId => { metrics: [{ts, data}], strategy: object|null } }
    this.store = new Map();
    // [{ userId, rating, comment, ts }]
    this.feedback = [];
  }

  /* ------------------------------------------------------------------ *
   *  Metrics
   * ------------------------------------------------------------------ */

  /**
   * Record a new metric event for a tactic.
   *
   * @param {string} tacticId
   * @param {Object} data  { impressions, clicks, conversions, … }
   */
  record(tacticId, data) {
    if (!tacticId || typeof tacticId !== 'string')
      throw new Error('tacticId must be a non‑empty string');
    if (!data || typeof data !== 'object')
      throw new Error('data must be a non‑null object');

    const entry = this.store.get(tacticId) || { metrics: [], strategy: null };
    entry.metrics.push({ ts: performance.now(), data });
    this.store.set(tacticId, entry);
  }

  /**
   * Return aggregated metrics for a tactic.
   *
   * @param {string} tacticId
   * @returns {Object} { count, total, avg, raw }
   */
  getEffectiveness(tacticId) {
    if (!tacticId || typeof tacticId !== 'string')
      throw new Error('tacticId must be a non‑empty string');

    const entry = this.store.get(tacticId);
    if (!entry) return { count: 0, total: {}, avg: {}, raw: [] };

    const { metrics } = entry;
    const count = metrics.length;
    const totals = {};
    const raw = metrics.map((m) => m.data);

    metrics.forEach(({ data }) => {
      Object.entries(data).forEach(([k, v]) => {
        if (typeof v === 'number') {
          totals[k] = (totals[k] || 0) + v;
        }
      });
    });

    const avg = {};
    Object.entries(totals).forEach(([k, v]) => {
      avg[k] = v / count;
    });

    return { count, total: totals, avg, raw };
  }

  /* ------------------------------------------------------------------ *
   *  Strategy
   * ------------------------------------------------------------------ */

  /**
   * Store a new strategy for a tactic.
   *
   * @param {string} tacticId
   * @param {Object} strategy
   */
  adjustStrategy(tacticId, strategy) {
    if (!tacticId || typeof tacticId !== 'string')
      throw new Error('tacticId must be a non‑empty string');
    if (!strategy || typeof strategy !== 'object')
      throw new Error('strategy must be a non‑null object');

    const entry = this.store.get(tacticId) || { metrics: [], strategy: null };
    entry.strategy = strategy;
    this.store.set(tacticId, entry);
  }

  /**
   * Retrieve the current strategy for a tactic.
   *
   * @param {string} tacticId
   * @returns {Object|null}
   */
  getStrategy(tacticId) {
    if (!tacticId || typeof tacticId !== 'string')
      throw new Error('tacticId must be a non‑empty string');

    const entry = this.store.get(tacticId);
    return entry ? entry.strategy : null;
  }

  /* ------------------------------------------------------------------ *
   *  Feedback
   * ------------------------------------------------------------------ */

  /**
   * Submit user feedback on the tracking feature.
   *
   * @param {Object} { userId, rating, comment? }
   */
  submitFeedback({ userId, rating, comment = '' }) {
    if (!userId || typeof userId !== 'string')
      throw new Error('userId must be a non‑empty string');
    if (typeof rating !== 'number')
      throw new Error('rating must be a number');

    this.feedback.push({
      userId,
      rating,
      comment,
      ts: performance.now(),
    });
  }

  /**
   * Return all feedback entries.
   *
   * @returns {Array}
   */
  getAllFeedback() {
    return [...this.feedback];
  }

  /* ------------------------------------------------------------------ *
   *  Utility
   * ------------------------------------------------------------------ */

  /**
   * Reset the entire store – useful for tests or nightly clean‑ups.
   */
  reset() {
    this.store.clear();
    this.feedback = [];
  }
}

// Export a singleton instance for global use
module.exports = new MarketingEffectivenessTracker();