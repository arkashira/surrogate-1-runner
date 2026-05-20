const express = require('express');
const bodyParser = require('body-parser');
const EventEmitter = require('events');
const validationRoutes = require('./routes/validation');

const app = express();
app.use(bodyParser.json());

// Global event emitter for real‑time updates
const projectEmitter = new EventEmitter();
app.set('projectEmitter', projectEmitter);

// Mount routes
app.use('/api/v1/validation', validationRoutes);

// Global error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal Server Error' });
});

module.exports = { app, projectEmitter };