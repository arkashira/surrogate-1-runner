/**
 * Utility helpers for surrogate‑1.
 *
 * - runAppleScript: low‑level wrapper around `osascript`.
 * - attemptAppleScriptPaste: high‑level “send Cmd+V” helper.
 * - delay: simple Promise‑based sleep.
 *
 * All functions are pure, return Promises, and never throw uncaught
 * exceptions – they log and return a boolean where appropriate.
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);
const logger = require('./logger');

/**
 * Execute an AppleScript snippet via `osascript`.
 *
 * @param {string} script   AppleScript source (may contain new‑lines).
 * @param {number} [timeoutMs=30000]  Max time to wait before killing the process.
 * @returns {Promise<string>} Resolves with trimmed stdout.
 * @throws {Error} If the process exits non‑zero or times out.
 */
async function runAppleScript(script, timeoutMs = 30000) {
  // Escape single quotes for the shell – safest way without a full‑blown shell‑escaper.
  const escaped = script.replace(/'/g, `'\\''`);
  const cmd = `osascript -e '${escaped}'`;

  try {
    const { stdout, stderr } = await execAsync(cmd, { timeout: timeoutMs });

    // `osascript` writes warnings to stderr but still exits 0.
    // Treat any non‑empty stderr as a warning, not a fatal error.
    if (stderr) {
      logger.warn('[utils] AppleScript wrote to stderr:', stderr.trim());
    }

    return stdout.trim();
  } catch (err) {
    // Normalise timeout vs. other exec errors.
    if (err.killed) {
      throw new Error(`AppleScript timed out after ${timeoutMs} ms`);
    }
    // Preserve the original message for diagnostics.
    throw new Error(`AppleScript execution failed: ${err.message}`);
  }
}

/**
 * High‑level helper that asks System Events to press Cmd+V.
 *
 * The AppleScript returns the literal string “OK” on success or
 * “ERROR:<msg>” on failure – we interpret that here.
 *
 * @returns {Promise<boolean>} true if the keystroke was accepted.
 */
async function attemptAppleScriptPaste() {
  const script = `
    try
      tell application "System Events"
        keystroke "v" using command down
      end tell
      return "OK"
    on error errMsg number errNum
      return "ERROR:" & errMsg
    end try
  `;

  try {
    const result = await runAppleScript(script, 15000); // 15 s is generous for UI interaction
    if (result === 'OK') {
      logger.info('[utils] AppleScript paste succeeded.');
      return true;
    }
    // Anything else is an error reported by the script itself.
    logger.warn('[utils] AppleScript reported error:', result);
    return false;
  } catch (err) {
    logger.error('[utils] AppleScript execution threw:', err.message);
    return false;
  }
}

/**
 * Simple Promise‑based sleep.
 *
 * @param {number} ms Milliseconds to wait.
 * @returns {Promise<void>}
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
  runAppleScript,
  attemptAppleScriptPaste,
  delay,
};