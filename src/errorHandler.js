/**
 * Centralised error handling for all surrogate‑1 integrations.
 *
 * Why?
 *  • Guarantees a uniform log format (easy to grep, ship to telemetry, etc.).
 *  • Gives callers a single error type (`IntegrationError`) they can `instanceof`
 *    check to decide whether to show a user‑friendly “integration failed” UI
 *    or to treat the error as a bug.
 *  • Preserves the original stack trace for debugging while still providing a
 *    clear, high‑level message.
 */

class IntegrationError extends Error {
  /**
   * @param {string} component   – Human‑readable name of the failing component
   *                               (e.g. "Resolver").
   * @param {Error}  original    – The raw error that was caught.
   */
  constructor(component, original) {
    super(`Integration failure in ${component}: ${original.message}`);
    this.name = 'IntegrationError';
    this.component = component;
    this.originalError = original;

    // Keep the original stack trace – it is invaluable when debugging.
    if (original.stack) {
      this.stack = `${this.stack}\nCaused by: ${original.stack}`;
    }
  }
}

/**
 * Log the error (console for now – replace with Winston/Pino/etc. in prod) and
 * re‑throw a wrapped `IntegrationError`.
 *
 * @param {Error}  err        – The caught error.
 * @param {string} component  – Component name for context.
 * @throws {IntegrationError}
 */
function handleIntegrationError(err, component = 'UnknownComponent') {
  // Structured logging placeholder – keep it simple but consistent.
  console.error(`[IntegrationError] ${component}: ${err.message}`);
  // Future‑proof: add telemetry here (e.g. Sentry, Datadog, etc.)

  // Throw the wrapped error so callers can `instanceof IntegrationError`.
  throw new IntegrationError(component, err);
}

module.exports = {
  IntegrationError,
  handleIntegrationError,
};