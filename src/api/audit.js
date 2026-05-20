const express = require('express');
const router = express.Router();
const { getAuditHistory, exportAuditHistory } = require('../services/auditService');

/**
 * GET /audit/:cellId/history?limit=100
 * Returns JSON audit history.
 */
router.get('/:cellId/history', async (req, res) => {
  const { cellId } = req.params;
  const limit = parseInt(req.query.limit, 10) || 100;

  try {
    const history = await getAuditHistory(cellId, limit);
    res.json(history);
  } catch (err) {
    console.error('GET /audit/:cellId/history error:', err);
    res.status(400).json({ error: err.message });
  }
});

/**
 * GET /audit/:cellId/export
 * Returns CSV attachment.
 */
router.get('/:cellId/export', async (req, res) => {
  const { cellId } = req.params;

  try {
    const csv = await exportAuditHistory(cellId);
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader(
      'Content-Disposition',
      `attachment; filename="audit_${cellId}.csv"`
    );
    res.send(csv);
  } catch (err) {
    console.error('GET /audit/:cellId/export error:', err);
    res.status(400).json({ error: err.message });
  }
});

module.exports = router;