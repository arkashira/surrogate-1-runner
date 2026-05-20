const db = require('../db');
const { format } = require('date-fns');

const MAX_LIMIT = 1000; // safety cap for export

/**
 * Retrieve audit history for a cell.
 * @param {string} cellId
 * @param {number} [limit=100] – max records to return
 * @returns {Promise<Array<{timestamp, userId, before, after}>>}
 */
async function getAuditHistory(cellId, limit = 100) {
  if (!cellId) throw new Error('cellId is required');

  const effectiveLimit = Math.min(limit, MAX_LIMIT);

  // SQL example – adjust for your DB
  const rows = await db.query(
    `
      SELECT changed_at, user_id, before_value, after_value
      FROM audit_logs
      WHERE cell_id = $1
      ORDER BY changed_at DESC
      LIMIT $2
    `,
    [cellId, effectiveLimit]
  );

  return rows.map(row => ({
    timestamp: format(row.changed_at, 'yyyy-MM-dd HH:mm:ss'),
    userId: row.user_id,
    before: row.before_value,
    after: row.after_value,
  }));
}

/**
 * Export audit history as a CSV string.
 * @param {string} cellId
 * @returns {Promise<string>} CSV content
 */
async function exportAuditHistory(cellId) {
  const history = await getAuditHistory(cellId, MAX_LIMIT);

  const header = ['Timestamp', 'User ID', 'Before', 'After'];
  const csvRows = [header];

  history.forEach(entry => {
    csvRows.push([
      entry.timestamp,
      entry.userId,
      entry.before,
      entry.after,
    ]);
  });

  // Escape CSV values
  const escape = v =>
    `"${String(v).replace(/"/g, '""')}"`;

  return csvRows
    .map(row => row.map(escape).join(','))
    .join('\n');
}

module.exports = { getAuditHistory, exportAuditHistory };