const express = require('express');
const router = express.Router();

/**
 * Health check endpoint to verify service availability.
 * Responds with HTTP 200 and "OK" to indicate operational status.
 */
router.get('/health', (req, res) => {
  res.status(200).send('OK');
});

module.exports = router;