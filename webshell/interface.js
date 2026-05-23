/**
 * Thin wrapper around child_process.exec that logs every command.
 * Exposes a Promise‑based API suitable for async/await.
 */

import { exec } from 'child_process';
import { logEntry } from './logging.js';
import util from 'util';

const execAsync = util.promisify(exec);

/**
 * Execute a shell command and log the activity.
 *
 * @param {string} cmd       – The command to run.
 * @param {string} [userId]  – Optional identifier of the caller.
 * @returns {Promise<string>} – Resolves with stdout.
 *
 * The function logs:
 *   - command
 *   - durationMs
 *   - stdout / stderr
 *   - success flag
 *   - errorMessage (if any)
 *
 * Logging failures are reported to console but do not block the command.
 */
export const executeCommand = async (cmd, userId) => {
  const start = Date.now();
  try {
    const { stdout, stderr } = await execAsync(cmd, { maxBuffer: 10 * 1024 * 1024 });
    const durationMs = Date.now() - start;

    await logEntry(
      {
        command: cmd,
        durationMs,
        stdout: stdout.trim(),
        stderr: stderr.trim(),
        success: true,
      },
      userId
    );

    return stdout;
  } catch (err) {
    const durationMs = Date.now() - start;

    // Log the failure – we still want the entry
    await logEntry(
      {
        command: cmd,
        durationMs,
        stdout: err.stdout?.trim() ?? '',
        stderr: err.stderr?.trim() ?? '',
        success: false,
        errorMessage: err.message,
      },
      userId
    );

    // Re‑throw so callers can handle it
    throw err;
  }
};

/**
 * Generic activity logger (e.g. login, logout, file upload).
 *
 * @param {string} activity – Human‑readable description.
 * @param {string} [userId] – Optional user identifier.
 */
export const logActivity = async (activity, userId) => {
  await logEntry({ activity }, userId);
};