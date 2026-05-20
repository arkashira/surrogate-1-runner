const express = require('express');
const app = express();
const updateServiceRouter = require('./routes/update-service');

app.use(express.json()); // Middleware to parse JSON bodies

app.use('/api/update-service', updateServiceRouter);

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});