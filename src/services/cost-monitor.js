/**
 * Cost Monitor Service
 *
 * Provides live polling of cost data every 5 minutes.
 * Consumers can register a callback to receive fresh data,
 * change the time range filter, and stop polling when no longer needed.
 */

let POLL_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes
let timerId = null;
let currentRange = 'hour'; // default time range
const listeners = new Set();

/**
 * Fetch cost data from the backend API for the given range.
 * Expected API: GET /api/cost?range=<range>
 *
 * @param {string} range - one of 'hour', 'day', 'week'
 * @returns {Promise<any>} Parsed JSON response
 */
function fetchCostData(range) {
  const url = `/api/cost?range=${encodeURIComponent(range)}`;
  return fetch(url, { credentials: 'same-origin' })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`Cost API responded with ${res.status}`);
      }
      return res.json();
    });
}

/**
 * Notify all registered listeners with fresh data.
 *
 * @param {any} data
 */
function notifyListeners(data) {
  listeners.forEach((cb) => {
    try {
      cb(data);
    } catch (e) {
      console.error('CostMonitor listener threw an error:', e);
    }
  });
}

/**
 * Perform a single poll: fetch data and broadcast it.
 */
function poll() {
  fetchCostData(currentRange)
    .then((data) => notifyListeners(data))
    .catch((err) => console.error('CostMonitor polling error:', err));
}

/**
 * Start polling.  The supplied callback will be invoked on every successful fetch.
 *
 * @param {(data:any)=>void} [callback] - optional listener to register immediately
 */
function start(callback) {
  if (callback) listeners.add(callback);
  if (!timerId) {
    // Immediate fetch so UI shows data without waiting 5 min
    poll();
    timerId = setInterval(poll, POLL_INTERVAL_MS);
  }
}

/**
 * Stop polling.  If a callback is supplied it is removed from the listener set.
 *
 * @param {(data:any)=>void} [callback]
 */
function stop(callback) {
  if (callback) listeners.delete(callback);
  // If no listeners remain, clean up the interval.
  if (listeners.size === 0 && timerId) {
    clearInterval(timerId);
    timerId = null;
  }
}

/**
 * Change the time‑range filter.  Triggers an immediate fetch with the new range.
 *
 * @param {string} range - 'hour' | 'day' | 'week'
 */
function setRange(range) {
  if (range !== currentRange) {
    currentRange = range;
    poll(); // fetch immediately for the new range
  }
}

// Export the public API
module.exports = {
  start,
  stop,
  setRange,
  // expose internals for unit‑testing (not part of the public contract)
  _internal: {
    fetchCostData,
    poll,
    listeners,
    getTimerId: () => timerId,
  },
};