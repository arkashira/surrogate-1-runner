const express = require('express');
const router = express.Router();
const validationUi = require('./validation');

router.use('/validation', validationUi);

module.exports = router;