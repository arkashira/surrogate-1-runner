const express = require('express');
const router = express.Router();
const config = require('./../config/validation');

router.get('/config', (req, res) => {
  res.json(config);
});

router.put('/config', (req, res) => {
  const { minStockLevel, maxStockCapacity } = req.body;
  config.minStockLevel = minStockLevel;
  config.maxStockCapacity = maxStockCapacity;
  res.json(config);
});

module.exports = router;