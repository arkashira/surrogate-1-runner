const express = require('express');
const router = express.Router();
const axios = require('axios');

// API endpoint to fetch user recordings
router.get('/recordings', async (req, res) => {
  try {
    const userId = req.user.id;
    const response = await axios.get(`https://example.com/recordings/${userId}`);
    const recordings = response.data;
    res.json(recordings);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Failed to fetch recordings' });
  }
});

// API endpoint to display user recordings
router.get('/recordings/:id', async (req, res) => {
  try {
    const recordingId = req.params.id;
    const response = await axios.get(`https://example.com/recordings/${recordingId}`);
    const recording = response.data;
    res.json(recording);
  } catch (error) {
    console.error(error);
    res.status(404).json({ message: 'Recording not found' });
  }
});

module.exports = router;