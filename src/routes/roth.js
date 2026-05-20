const express = require('express');
const router = express.Router();
const rothController = require('../controllers/rothController');

/**
 * POST /roth/state
 * Persist wizard state
 */
router.post('/state', rothController.saveWizardState);

/**
 * GET /roth/state/:id
 * Retrieve persisted wizard state
 */
router.get('/state/:id', rothController.getWizardState);

module.exports = router;