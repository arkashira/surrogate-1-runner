const express = require('express');
const prometheusExporter = require('./monitoring/prometheusExporter');

const app = express();

// Add your existing API routes here
app.get('/api/endpoint', (req, res) => {
  res.json({ message: 'API response' });
});

// Mount Prometheus exporter
app.use('/metrics', prometheusExporter);

module.exports = app;