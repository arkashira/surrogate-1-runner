const express = require('express');
const router = express.Router();

const validationMiddleware = require('./validation');

router.use('/validation', validationMiddleware);

module.exports = router;