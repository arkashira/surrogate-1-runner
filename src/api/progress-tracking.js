const express = require('express');
const router = express.Router();
const ProgressTracking = require('../models/progress-tracking');

router.get('/user/:userId', async (req, res) => {
  try {
    const progress = await ProgressTracking.findOne({ userId: req.params.userId });
    if (!progress) return res.status(404).send('User not found');
    res.send(progress);
  } catch (err) {
    res.status(500).send('Server error');
  }
});

router.post('/user/:userId', async (req, res) => {
  try {
    const progress = new ProgressTracking(req.body);
    await progress.save();
    res.send(progress);
  } catch (err) {
    res.status(500).send('Server error');
  }
});

module.exports = router;