const { error: logError } = require('./logger');

/**
 * Centralised error handling.
 *
 * @param {Error|string} errOrMsg – Either an Error object or a short message.
 * @param {Object} [context={}] – Arbitrary key/value pairs that describe where/why the error happened.
 * @throws {Error} – The original (or a wrapped) error, enriched with `context`.
 */
function handleError(errOrMsg, context = {}) {
  const err = errOrMsg instanceof Error ? errOrMsg : new Error(String(errOrMsg));

  // Attach the context for upstream consumers.
  err.context = context;

  // Build a readable log line.
  const ctxString = Object.entries(context)
    .map(([k, v]) => `${k}=${v}`)
    .join(' ');
  const logMsg = `Resolver Error: ${err.message}${ctxString ? ' | ' + ctxString : ''}`;

  // Persist the error.
  logError(logMsg);

  // Re‑throw so callers can decide (retry, abort, etc.).
  throw err;
}

module.exports = { handleError };