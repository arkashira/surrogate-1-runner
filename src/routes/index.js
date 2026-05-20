const express = require('express');
const router = express.Router();

// Existing route imports (if any)
// const otherRoutes = require('./other');
// router.use('/other', otherRoutes);

// Import and mount Roth wizard routes
const rothRoutes = require('./roth');
router.use('/roth', rothRoutes);

module.exports = router;