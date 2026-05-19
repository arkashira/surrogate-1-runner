const express = require('express');
const taskController = require('../controllers/taskController');

const router = express.Router();

router.put('/tasks/:id/status', taskController.updateStatus);

module.exports = router;