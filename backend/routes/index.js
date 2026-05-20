const express = require('express');
const router = express.Router();

const templateRoutes = require('./templateRoutes');

router.use('/templates', templateRoutes);

// Health‑check
router.get('/health', (_, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

module.exports = router;