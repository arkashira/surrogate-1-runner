const express = require('express');
const app = express();
const feedbackRouter = require('./feedback');

app.use('/api/feedback', feedbackRouter);

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});