const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const os = require('os');
const { promisify } = require('util');
const config = require('./config.json');

const LOG_DIR = path.resolve(config.auditLogDir);
const REPORT_DIR = path.resolve(config.reportDir);

if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
if (!fs.existsSync(REPORT_DIR)) fs.mkdirSync(REPORT_DIR, { recursive: true });

const appendFile = promisify(fs.appendFile);
const writeFile = promisify(fs.writeFile);
const readFile = promisify(fs.readFile);

/**
 * In‑memory index: { date: [auditId, ...] }
 * Keeps the auditStore small; full data lives on disk.
 */
const auditIndex = new Map();

/**
 * Generate a cryptographically‑strong audit ID.
 */
function generateAuditId() {
  return crypto.randomBytes(16).toString('hex');
}

/**
 * Persist an audit record to the daily JSONL file.
 * The file is named YYYY-MM-DD.log
 */
async function persistAudit(record) {
  const date = record.timestamp.slice(0, 10); // YYYY-MM-DD
  const filePath = path.join(LOG_DIR, `${date}.log`);
  const line = JSON.stringify(record) + os.EOL;
  await appendFile(filePath, line, 'utf8');

  // Update index
  if (!auditIndex.has(date)) auditIndex.set(date, []);
  auditIndex.get(date).push(record.auditId);
}

/**
 * Record an audit event.
 * @param {Object} params
 * @param {string} params.user
 * @param {string} params.command
 * @param {string} [params.output]
 * @param {Error}   [params.error]
 */
async function recordAudit({ user, command, output = '', error = null }) {
  const auditId = generateAuditId();
  const entry = {
    auditId,
    timestamp: new Date().toISOString(),
    user,
    command,
    output,
    error: error ? error.message : null,
    hostname: os.hostname(),
  };

  await persistAudit(entry);

  // Notify subscribers
  if (Array.isArray(onAudit.callbacks)) {
    onAudit.callbacks.forEach(cb => cb(entry));
  }

  return entry;
}

/**
 * Generate a compliance report for a date range.
 * @param {string} startISO - inclusive
 * @param {string} endISO   - exclusive
 * @returns {Promise<Object[]>}
 */
async function generateReport(startISO, endISO) {
  const start = new Date(startISO);
  const end   = new Date(endISO);
  const results = [];

  for (const [date, ids] of auditIndex.entries()) {
    const fileDate = new Date(date);
    if (fileDate < start || fileDate >= end) continue;

    const filePath = path.join(LOG_DIR, `${date}.log`);
    const data = await readFile(filePath, 'utf8');
    const lines = data.trim().split(/\r?\n/);
    for (const line of lines) {
      const rec = JSON.parse(line);
      const ts = new Date(rec.timestamp);
      if (ts >= start && ts < end) results.push(rec);
    }
  }
  return results;
}

/**
 * Export a report to a pretty‑printed JSON file.
 * @param {string} outputPath
 * @param {Object[]} data
 */
async function exportReport(outputPath, data) {
  const json = JSON.stringify(data, null, 2);
  await writeFile(outputPath, json, 'utf8');
}

/**
 * Hook for external tools to subscribe to audit events.
 * @param {(Object)=>void} callback
 */
function onAudit(callback) {
  if (!Array.isArray(onAudit.callbacks)) onAudit.callbacks = [];
  onAudit.callbacks.push(callback);
}

module.exports = {
  recordAudit,
  generateReport,
  exportReport,
  onAudit,
};