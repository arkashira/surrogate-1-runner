const express = require('express');
const router = express.Router();
const { sendAlert } = require('../logic/alert-sending');

router.post('/alert', async (req, res) => {
  try {
    const { email, message } = req.body;
    if (!email || !message) {
      return res.status(400).send('Email and message are required.');
    }

    await sendAlert(email, message);
    res.status(200).send('Alert sent successfully');
  } catch (error) {
    console.error('Error processing alert request:', error);
    res.status(500).send('Failed to send alert.');
  }
});

module.exports = router;