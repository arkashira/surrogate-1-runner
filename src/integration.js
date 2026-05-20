/**
 * Integration layer for the Resolver inside surrogate‑1.
 *
 * Public API:
 *   - integrateResolver(): Promise<object> | object
 *   - getResolver(): object
 *
 * All errors flow through `handleIntegrationError`, guaranteeing a
 * consistent `IntegrationError` shape.
 */

const path = require('path');
const { handleIntegrationError } = require('./errorHandler');

let resolverInstance = null;

/**
 * Load the resolver module **dynamically** so the rest of the codebase
 * does not fail at `require` time if the resolver is missing or broken.
 *
 * @returns {object} The raw resolver export (usually a class).
 * @throws {Error} Propagates any require‑time failure.
 */
function loadResolver() {
  const resolverPath = path.resolve(__dirname, '../resolver/index.js');
  // eslint-disable-next-line global-require, import/no-dynamic-require
  return require(resolverPath);
}

/**
 * Initialise the resolver and store the singleton instance.
 *
 * Supports both:
 *   - sync constructors + optional `init()` returning nothing
 *   - async `init()` returning a Promise
 *
 * @returns {Promise<object>|object} The ready‑to‑use resolver.
 * @throws {IntegrationError} on any load/initialisation problem.
 */
function integrateResolver() {
  try {
    const Resolver = loadResolver();

    // If the resolver exports a factory function instead of a class,
    // we still support it – just call it.
    resolverInstance = typeof Resolver === 'function' ? new Resolver() : Resolver;

    // If there is an async init step, wait for it.
    if (typeof resolverInstance.init === 'function') {
      const maybePromise = resolverInstance.init();
      // Normalise to a Promise – callers can `await` safely.
      return Promise.resolve(maybePromise).then(() => resolverInstance);
    }

    // No async init → return the instance directly.
    return resolverInstance;
  } catch (err) {
    // Anything that bubbles up (require error, constructor error, etc.)
    // is turned into a first‑class IntegrationError.
    handleIntegrationError(err, 'Resolver');
  }
}

/**
 * Retrieve the already‑initialised resolver.
 *
 * @returns {object} The resolver singleton.
 * @throws {IntegrationError} if `integrateResolver()` has not been called yet.
 */
function getResolver() {
  if (!resolverInstance) {
    const err = new Error(
      'Resolver has not been initialised. Call integrateResolver() first.'
    );
    handleIntegrationError(err, 'Resolver');
  }
  return resolverInstance;
}

module.exports = {
  integrateResolver,
  getResolver,
};