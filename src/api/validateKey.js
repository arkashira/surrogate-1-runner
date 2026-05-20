const express = require('express');
const router = express.Router();
const { isValidApiKey } = require('../utils/validators');

/**
 * POST /validate-key
 * Body: { apiKey: string }
 * Response:
 *   200 { valid: true }
 *   400 { valid: false, error: string }
 */
router.post('/', (req, res) => {
  const { apiKey } = req.body;

  if (typeof apiKey !== 'string') {
    return res.status(400).json({ valid: false, error: 'apiKey must be a string' });
  }

  if (isValidApiKey(apiKey)) {
    return res.json({ valid: true });
  }

  return res.status(400).json({ valid: false, error: 'Invalid API key format' });
});

module.exports = router;