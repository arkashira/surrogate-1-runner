const express = require('express');
const router = express.Router();
const patternController = require('../controllers/patternController');

router.post('/submit', patternController.submitPattern);

module.exports = router;