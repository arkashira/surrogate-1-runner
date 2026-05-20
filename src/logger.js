const fs   = require('fs');
const path = require('path');

const LOG_FILE = path.join(__dirname, 'error.log');

/**
 * Append a line to the log file and also write to stderr.
 * @param {string} message – Human‑readable log line (already formatted).
 */
function error(message) {
  const line = `${new Date().toISOString()} ${message}\n`;
  try {
    fs.appendFileSync(LOG_FILE, line, { encoding: 'utf8' });
  } catch (fsErr) {
    // If the file can’t be written we still want the message visible.
    console.error('⚠️  Logger failed:', fsErr);
  }
  // Always echo to the console so Docker/K8s log collectors see it.
  console.error(message);
}

module.exports = { error };