const express = require('express');
const router = express.Router();

// Mock data for recordings
const recordings = [
  { title: 'Session 1', date: '2023-05-01', duration: 30 },
  { title: 'Session 2', date: '2023-05-02', duration: 45 },
  // Add more sessions as needed
];

router.get('/', (req, res) => {
  res.json(recordings);
});

module.exports = router;