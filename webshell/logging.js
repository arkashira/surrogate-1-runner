/**
 * Tamper‑evident, daily rotating JSON‑Lines logger.
 *
 * Each log entry is a JSON object that contains:
 *   - timestamp
 *   - userId (optional)
 *   - command / activity
 *   - stdout / stderr (if a command)
 *   - success flag
 *   - errorMessage (if any)
 *   - prevHash   – SHA‑256 of the previous entry
 *   - entryHash  – SHA‑256 of this entry + prevHash
 *
 * The logger keeps a 30‑day retention window.
 */

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';

const LOG_DIR = path.resolve(process.cwd(), 'logs');
const LOG_RETENTION_DAYS = 30;

// Ensure the log directory exists on startup
await fs.mkdir(LOG_DIR, { recursive: true });

/** Helper: SHA‑256 of a string */
const sha256 = (data) => crypto.createHash('sha256').update(data, 'utf8').digest('hex');

/** Get the current log file path (YYYY-MM-DD.jsonl) */
const getLogFilePath = () => {
  const dateStr = new Date().toISOString().slice(0, 10);
  return path.join(LOG_DIR, `${dateStr}.jsonl`);
};

/**
 * Read the hash of the last log entry in a file.
 * Returns a 64‑char hex string of zeros if the file is empty / missing.
 */
const getPrevHash = async (logFile) => {
  try {
    const stats = await fs.stat(logFile);
    if (stats.size === 0) return '0'.repeat(64);

    // Read the last 1 kB – enough to contain the last line
    const buffer = Buffer.alloc(1024);
    const fd = await fs.open(logFile, 'r');
    try {
      const { bytesRead } = await fd.read(buffer, 0, 1024, Math.max(0, stats.size - 1024));
      const tail = buffer.slice(0, bytesRead).toString('utf8');
      const lines = tail.split('\n').filter(Boolean);
      const lastLine = lines[lines.length - 1];
      if (!lastLine) return '0'.repeat(64);
      const lastObj = JSON.parse(lastLine);
      return lastObj.entryHash ?? '0'.repeat(64);
    } finally {
      await fd.close();
    }
  } catch {
    // File missing or unreadable
    return '0'.repeat(64);
  }
};

/**
 * Append a single log entry.
 * @param {Object} entry - Plain object containing the event data.
 * @param {string} [userId] - Optional user identifier.
 */
export const logEntry = async (entry, userId) => {
  const logFile = getLogFilePath();
  const prevHash = await getPrevHash(logFile);

  const timestamp = new Date().toISOString();
  const payload = JSON.stringify({ timestamp, userId, ...entry });
  const entryHash = sha256(payload + prevHash);

  const logLine = JSON.stringify({
    timestamp,
    userId,
    ...entry,
    prevHash,
    entryHash,
  });

  await fs.appendFile(logFile, logLine + '\n', 'utf8');
};

/**
 * Remove log files older than the retention window.
 * Called once on startup – can be scheduled if desired.
 */
export const cleanupOldLogs = async () => {
  const files = await fs.readdir(LOG_DIR);
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - LOG_RETENTION_DAYS);

  await Promise.all(
    files.map(async (file) => {
      const filePath = path.join(LOG_DIR, file);
      const stats = await fs.stat(filePath);
      if (stats.mtime < cutoff) await fs.unlink(filePath);
    })
  );
};

// Run cleanup immediately on module load
cleanupOldLogs().catch((e) => console.error('Log cleanup failed', e));