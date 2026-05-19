/**
 * Helper functions that build the payload objects expected by the resolver.
 * Keeping them in a dedicated module makes them easy to unit‑test and reuse
 * across the integration suite.
 */

function buildAxDirectPayload(url) {
  return {
    url,
    method: 'GET',
    // any other fields the resolver expects for an AX direct attempt
  };
}

function buildCgEventPayload(key = 'V', modifiers = ['command']) {
  return {
    event: 'keyDown',
    key,
    modifiers,
  };
}

function buildAppleScriptPayload(script) {
  return { script };
}

/**
 * Small validation utilities – useful for both the resolver implementation
 * and the unit tests.
 */
function validateEventType(type) {
  return ['AX', 'CGEvent', 'AppleScript'].includes(type);
}

function formatTimestamp(ts) {
  return new Date(ts).toISOString();
}

module.exports = {
  buildAxDirectPayload,
  buildCgEventPayload,
  buildAppleScriptPayload,
  validateEventType,
  formatTimestamp,
};