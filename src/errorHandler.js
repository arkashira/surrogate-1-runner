/**
 * Centralised error handling for the resolver.
 *
 * - Writes a human‑readable line to `resolver-errors.log`.
 * - Writes a JSON‑line to the same file (appended after the text line) for
 *   automated analysis.
 * - Emits a placeholder metric (hooked to a global `__metrics__` object if
 *   present).
 * - Returns a boolean indicating whether the caller should retry.
 *
 * The module is deliberately lightweight: all I/O is synchronous and
 * guarded so that a logging failure never crashes the process.
 */

const fs = require('fs');
const path = require('path');

const LOG_DIR = path.resolve(__dirname, '../../logs');
const LOG_FILE = path.join(LOG_DIR, 'resolver-errors.log');

/**
 * Ensure the log directory exists (once, synchronously).
 */
function ensureLogDir() {
  if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
  }
}
ensureLogDir();

/**
 * Write a single line (text) to the log file.
 * @param {string} line
 */
function writeTextLine(line) {
  try {
    fs.appendFileSync(LOG_FILE, line + '\n', { encoding: 'utf8' });
  } catch (e) {
    // Swallow – we never want logging to bring down the resolver.
    console.error('⚠️  Failed to write text log entry:', e);
  }
}

/**
 * Write a JSON‑line to the log file.
 * @param {Object} obj
 */
function writeJsonLine(obj) {
  try {
    const line = JSON.stringify(obj);
    fs.appendFileSync(LOG_FILE, line + '\n', { encoding: 'utf8' });
  } catch (e) {
    console.error('⚠️  Failed to write JSON log entry:', e);
  }
}

/**
 * Central error handler.
 *
 * @param {Error} error   The caught error.
 * @param {Object} [context={}]  Optional extra data:
 *        - operation: string identifying the step (e.g. 'primaryAttempt',
 *                     'appleScriptAttempt')
 *        - attempt:   numeric count of how many times this operation has run
 *        - extra:     any additional free‑form data you want persisted
 *
 * @returns {boolean}  `true` if the caller should retry, `false` otherwise.
 */
function handleError(error, context = {}) {
  const timestamp = new Date().toISOString();

  // ---------- Human‑readable line ----------
  const textEntry = `[${timestamp}] [${context.operation || 'unknown'}] ${error.stack ||
    error.message ||
    String(error)}`;
  writeTextLine(textEntry);

  // ---------- Structured JSON line ----------
  const jsonEntry = {
    timestamp,
    operation: context.operation || 'unknown',
    attempt: context.attempt ?? 0,
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack,
    },
    extra: context.extra || {},
  };
  writeJsonLine(jsonEntry);

  // ---------- Metric hook (optional) ----------
  if (global.__metrics__) {
    global.__metrics__.increment('resolver.errors', 1, {
      operation: jsonEntry.operation,
      type: error.name,
    });
  }

  // ---------- Retry policy ----------
  // AppleScript failures are considered non‑retryable.
  if (jsonEntry.operation === 'appleScriptAttempt') {
    return false;
  }

  // For any other operation we allow **one** retry (attempt 0 → retry once).
  return (jsonEntry.attempt ?? 0) < 1;
}

module.exports = {
  handleError,
};