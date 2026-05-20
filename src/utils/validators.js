/**
 * Simple API key validator.
 * Rules:
 *   - Must be a string.
 *   - Length between 20 and 100 characters (inclusive).
 *   - Only alphanumeric characters, hyphens, or underscores.
 *
 * @param {string} key
 * @returns {boolean}
 */
function isValidApiKey(key) {
  if (typeof key !== 'string') return false;
  const trimmed = key.trim();
  if (trimmed.length < 20 || trimmed.length > 100) return false;
  return /^[A-Za-z0-9_-]+$/.test(trimmed);
}

module.exports = {
  isValidApiKey,
};