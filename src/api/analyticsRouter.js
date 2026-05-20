/**
 * Express router that exposes the analytics payload at /api/analytics.
 *
 * It uses the pure engine from src/dashboard/analytics.js.
 */

const express = require('express');
const { loadRecords, computeAnalytics } = require('../dashboard/analytics');

const router = express.Router();

/**
 * GET /api/analytics
 * Returns JSON with the computed metrics.
 */
router.get('/', (req, res) => {
  try {
    const records = loadRecords();
    const payload = computeAnalytics(records);
    res.json(payload);
  } catch (err) {
    console.error('Analytics route error:', err);
    res.status(500).json({ error: 'Unable to compute analytics' });
  }
});

module.exports = router;