const express = require('express');
const router = express.Router();
const recordingRouter = require('./recording');

router.use('/api/recordings', recordingRouter);

module.exports = router;