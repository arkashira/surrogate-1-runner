const express = require('express');
const router = express.Router();
const cloudCostService = require('../services/cloudCostService');

router.get('/', async (req, res) => {
  try {
    const costs = await cloudCostService.getCurrentCosts();
    res.json(costs);
  } catch (error) {
    console.error('Error fetching cloud costs:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;