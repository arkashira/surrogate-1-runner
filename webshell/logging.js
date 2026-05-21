/**
 * Public API for the web‑shell logger.
 *
 * Usage:
 *   const { logCommand } = require('./logging');
 *   logCommand({ user: 'alice', command: 'ls -la', sessionId: 'sess‑123' });
 */

const storage = require('./storage');

/**
 * Log a shell command.
 *
 * @param {Object} params
 * @param {string} params.user       Username or session ID
 * @param {string} params.command    Raw shell command
 * @param {string} [params.sessionId] Optional unique session identifier
 */
async function logCommand({ user, command, sessionId = null }) {
  if (!user || !command) {
    // Defensive: avoid logging incomplete records
    return;
  }

  const entry = { user, command, sessionId };
  await storage.appendEntry(entry);
}

module.exports = { logCommand };