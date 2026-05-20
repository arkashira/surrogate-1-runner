const express = require('express');
const router = express.Router();
const AuditLog = require('../models/auditLog');
const { check, validationResult } = require('express-validator');

// Search and filter audit logs
router.get('/search', [
  check('modelId').optional().isString(),
  check('startDate').optional().isISO8601().toDate(),
  check('endDate').optional().isISO8601().toDate(),
  check('input').optional().isString(),
  check('output').optional().isString(),
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { modelId, startDate, endDate, input, output } = req.query;
    const query = {};

    if (modelId) {
      query.modelId = modelId;
    }

    if (startDate || endDate) {
      query.timestamp = {};
      if (startDate) {
        query.timestamp.$gte = new Date(startDate);
      }
      if (endDate) {
        query.timestamp.$lte = new Date(endDate);
      }
    }

    if (input) {
      query.input = { $regex: input, $options: 'i' };
    }

    if (output) {
      query.output = { $regex: output, $options: 'i' };
    }

    const auditLogs = await AuditLog.find(query).sort({ timestamp: -1 });
    res.json(auditLogs);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server Error' });
  }
});

module.exports = router;