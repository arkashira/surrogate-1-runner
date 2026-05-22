const express = require('express');
const router = express.Router();
const { processSpec } = require('../controllers/specEditorController');

router.post('/process-spec', processSpec);

module.exports = router;