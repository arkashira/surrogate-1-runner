const express = require('express');
const router = express.Router();
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json();

let feedbackData = [];

router.post('/submit', jsonParser, (req, res) => {
  const { issue, suggestion, rating } = req.body;

  if (!issue && !suggestion && rating === undefined) {
    return res.status(400).send('At least one field must be filled.');
  }

  const feedback = {
    issue,
    suggestion,
    rating,
    timestamp: new Date().toISOString()
  };

  feedbackData.push(feedback);

  // Save feedback data to a file or database here
  console.log('Feedback received:', feedback);

  res.status(200).send('Feedback submitted successfully.');
});

module.exports = router;