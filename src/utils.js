/**
 * Centralised utilities for the surrogate‑1 product.
 * - File‑based logging (INFO / ERROR) with console fallback.
 * - async wrapper that logs and re‑throws.
 */

const fs   = require('fs');
const path = require('path');

const LOG_FILE = path.resolve(__dirname, '../../logs/surrogate.log');

/**
 * Append a formatted line to the log file.
 */
function writeLog(level, message, error) {
  const ts   = new Date().toISOString();
  const base = `[${ts}] [${level}] ${message}`;
  const line = error ? `${base}\n${error.stack}` : base;

  try {
    fs.appendFileSync(LOG_FILE, line + '\n');
  } catch (_) {
    // Never silence a logging failure – fall back to console.
    console.error('⚠️  Logging to file failed:', line);
  }
}

/** Public helpers */
function logInfo(message)  { writeLog('INFO',  message); }
function logError(message, err) { writeLog('ERROR', message, err); }

/**
 * Wrap an async function so that any uncaught error is logged
 * (with the function name) before being re‑thrown.
 */
function withErrorHandling(fn) {
  return async (...args) => {
    try {
      return await fn(...args);
    } catch (err) {
      logError(`Unhandled error in ${fn.name || '<anonymous>'}`, err);
      throw err;               // preserve original stack for callers
    }
  };
}

module.exports = {
  logInfo,
  logError,
  withErrorHandling,
};