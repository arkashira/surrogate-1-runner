const express = require('express');
const router = express.Router();
const { signup } = require('../controllers/authController');

// Advisor sign-up endpoint
router.post('/signup', signup);

module.exports = router;