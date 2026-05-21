/**
 * Storage layer for tamper‑evident logs.
 *
 * Features:
 *   • Daily log files under LOG_DIR (default: /var/log/webshell)
 *   • Strict permissions (0700 dir, 0600 file)
 *   • Atomic async appends
 *   • Helper to read the last hash
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');
const os = require('os');

/* ---------- Configuration ---------- */
const LOG_DIR = process.env.LOG_DIR || '/var/log/webshell';
const LOG_FILE_PREFIX = 'webshell-';          // e.g. webshell-2024-05-12.log
const LOG_FILE_EXT = '.log';

/* ---------- Helpers ---------- */

/**
 * Ensure the log directory exists with 0700 permissions.
 */
async function ensureLogDir() {
  try {
    await fs.mkdir(LOG_DIR, { mode: 0o700, recursive: true });
  } catch (err) {
    if (err.code !== 'EEXIST') throw err;
  }
}

/**
 * Return the full path to today’s log file.
 */
function getLogFilePath() {
  const date = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  return path.join(LOG_DIR, `${LOG_FILE_PREFIX}${date}${LOG_FILE_EXT}`);
}

/**
 * Compute a SHA‑256 hash of a string.
 * @param {string} data
 * @returns {string} hex digest
 */
function computeHash(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

/**
 * Read the last line of the log file and return its `currentHash`.
 * @returns {Promise<string|null>} hash or null if file empty / missing
 */
async function getLastHash() {
  const filePath = getLogFilePath();
  try {
    const data = await fs.readFile(filePath, 'utf8');
    const lines = data.trim().split(/\r?\n/).filter(Boolean);
    if (lines.length === 0) return null;
    const last = JSON.parse(lines[lines.length - 1]);
    return last.currentHash || null;
  } catch (err) {
    if (err.code === 'ENOENT') return null; // file does not exist
    throw new Error(`Failed to read last hash: ${err.message}`);
  }
}

/**
 * Append a new log entry atomically.
 * @param {Object} entry – payload without hashes
 */
async function appendEntry(entry) {
  await ensureLogDir();

  const prevHash = await getLastHash() ?? '';
  const timestamp = new Date().toISOString();

  const payload = { timestamp, ...entry };
  const payloadStr = JSON.stringify(payload);

  const currentHash = computeHash(prevHash + payloadStr);

  const record = {
    ...payload,
    prevHash: prevHash || null,
    currentHash,
  };

  const line = JSON.stringify(record) + os.EOL;

  const filePath = getLogFilePath();
  try {
    await fs.appendFile(filePath, line, { mode: 0o600 });
  } catch (err) {
    throw new Error(`Failed to append log entry: ${err.message}`);
  }
}

/* ---------- Exports ---------- */
module.exports = {
  appendEntry,
  getLastHash,
  getLogFilePath,
  _computeHash: computeHash, // for tests
};