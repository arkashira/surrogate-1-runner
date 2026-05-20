const express = require('express');
const router = express.Router();
const labsController = require('../controllers/labsController');

/**
 * @route POST /api/labs/launch
 * @desc Launch lab instance from template
 * @access Public
 */
router.post('/launch', labsController.launchLab);

module.exports = router;