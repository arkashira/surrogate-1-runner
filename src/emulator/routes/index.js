const express = require('express');
const eventsRouter = require('./events');

const app = express();

// Middleware
app.use(express.json({ limit: '10mb' }));

// Routes
app.use('/api/v1/events', eventsRouter);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', version: '1.0.0' });
});

module.exports = app;