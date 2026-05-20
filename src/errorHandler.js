const logger = require('./logger');
const { notifySupportTeam } = require('./notifier'); // see note below
const { implementFallbackResolution } = require('./fallback');

/**
 * Central error‑handling entry point for AX‑direct failures.
 *
 * @param {Error} error – The exception caught in resolver.js
 * @returns {Promise<void>}
 */
async function handleAxDirectError(error) {
  logger.error('🛑 AX‑direct resolution failed: %s', error.message, { error });

  // 1️⃣ Log detailed diagnostics (already done by winston)
  logErrorDetails(error);

  // 2️⃣ Notify the appropriate team / system
  await notifySupportTeam(error);

  // 3️⃣ Run a safe fallback so the request does not hang forever
  await implementFallbackResolution();
}

/**
 * Separate function makes unit‑testing easier.
 */
function logErrorDetails(error) {
  // Structured logging already captured stack & metadata.
  // Add any domain‑specific fields you need, e.g. requestId, userId.
  logger.debug('Error details: %O', {
    name: error.name,
    message: error.message,
    stack: error.stack,
    // custom fields can be merged here
  });
}

module.exports = { handleAxDirectError };