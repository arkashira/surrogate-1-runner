const express = require('express');
const router = express.Router();
const IntegrationManager = require('../logic/integration');
const config = require('../config');

// Initialise manager with persisted config
let manager = new IntegrationManager(config.getIntegrationConfig());

/**
 * GET /integration/status
 * Returns JSON indicating whether the external service is reachable.
 */
router.get('/status', async (req, res) => {
  const reachable = await manager.testConnection();
  res.json({ status: reachable ? 'connected' : 'unreachable' });
});

/**
 * POST /integration/configure
 * Body: { endpoint, username, password }
 * Updates the integration configuration securely.
 */
router.post('/configure', express.json(), (req, res) => {
  const { endpoint, username, password } = req.body || {};

  if (!endpoint || !username || !password) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Persist new configuration
  config.setIntegrationConfig({ endpoint, username, password });

  // Re‑instantiate manager with fresh config
  manager = new IntegrationManager(config.getIntegrationConfig());

  res.json({ message: 'Integration configuration updated' });
});

/**
 * GET /integration/config
 * Returns the current (non‑sensitive) configuration.
 */
router.get('/config', (req, res) => {
  res.json(manager.getConfig());
});

module.exports = router;