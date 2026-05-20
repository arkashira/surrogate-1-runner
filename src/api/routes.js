const express = require('express');
const router = express.Router();
const creditController = require('./creditController');

// Credit balance routes
router.get('/credits/balance', creditController.getBalance.bind(creditController));
router.get('/credits/history', creditController.getHistory.bind(creditController));
router.get('/credits/dashboard', creditController.getDashboard.bind(creditController));

// Health check
router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

module.exports = router;