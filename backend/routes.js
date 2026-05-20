const express = require('express');
const Dashboard = require('./dashboard');

const router = express.Router();
const dashboard = new Dashboard();

router.get('/security', async (req, res) => {
  await dashboard.update();
  res.json({ status: dashboard.getSecurityStatus() });
});

module.exports = router;