/**
 * Unified analytics logger.
 *
 * • In‑memory array → ultra‑fast reads for dashboards & tests.
 * • Append‑only JSON‑lines file → persistence & audit trail.
 *
 * Exported as a **singleton** so the whole app shares the same store.
 */

const fs = require('fs');
const path = require('path');

// ---------- 1️⃣ File‑backed persistence ----------
const LOG_DIR = path.resolve(__dirname, '../../logs');
const LOG_FILE = path.join(LOG_DIR, 'analytics.log');

// Ensure the directory exists (idempotent)
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

/**
 * Append a single JSON‑encoded line to the log file.
 * Synchronous I/O is acceptable for a low‑volume analytics stream
 * and guarantees ordering (no race conditions with async writes).
 *
 * @param {Object} lineObj
 */
function appendToFile(lineObj) {
  const line = JSON.stringify(lineObj);
  try {
    fs.appendFileSync(LOG_FILE, line + '\n', { encoding: 'utf8' });
  } catch (err) {
    // Never let a logging failure bring down the app.
    console.error('[AnalyticsLogger] Failed to write to file:', err);
  }
}

/**
 * Load *all* persisted events from the file.
 * Returns an empty array if the file does not exist or is empty.
 *
 * @returns {Object[]}
 */
function readAllFromFile() {
  if (!fs.existsSync(LOG_FILE)) return [];

  const raw = fs.readFileSync(LOG_FILE, { encoding: 'utf8' });
  if (!raw.trim()) return [];

  return raw
    .trim()
    .split('\n')
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch (_) {
        // Corrupt line – skip but keep the process alive.
        return null;
      }
    })
    .filter(Boolean);
}

// ---------- 2️⃣ In‑memory store ----------
class AnalyticsLogger {
  constructor() {
    // Load persisted events into memory on startup.
    this.events = readAllFromFile(); // [{ ts, type, payload, ... }]
  }

  /**
   * Log an event to **both** stores.
   *
   * @param {string} type    – e.g. "user_activity"
   * @param {Object} payload – arbitrary data (must be JSON‑serialisable)
   * @returns {Object} the full event object that was stored
   */
  logEvent(type, payload = {}) {
    const event = {
      ts: new Date().toISOString(),
      type,
      payload,
    };

    // 1️⃣ In‑memory
    this.events.push(event);

    // 2️⃣ File
    appendToFile(event);

    // Helpful stdout for dev / CI visibility
    console.log(`[Analytics] ${type}`, event);
    return event;
  }

  /** Return a **shallow copy** of the in‑memory array – callers cannot mutate the store. */
  getAllEvents() {
    return this.events.slice();
  }

  /** Remove everything – handy for test suites. */
  clear() {
    this.events = [];
    // Truncate the file as well (best‑effort, ignore errors)
    try {
      fs.truncateSync(LOG_FILE, 0);
    } catch (_) {}
  }
}

// Export a singleton instance
module.exports = new AnalyticsLogger();