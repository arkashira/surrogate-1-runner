const express = require('express');
const { Registry } = require('prom-client');

const registry = new Registry();
registry.setDefaultLabels({ app: 'surrogate-1' });

// Define Prometheus metrics
const apiRequestCost = new registry.Gauge({
  name: 'api_request_cost',
  help: 'Cost associated with each API request',
  labelNames: ['endpoint', 'method']
});

const app = express();

app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', registry.contentType);
    res.send(await registry.metrics());
  } catch (err) {
    console.error('Error serving metrics:', err);
    res.status(500).send('Error serving metrics');
  }
});

// Middleware to track cost per API request
function trackApiRequestCost(req, res, next) {
  const startTime = Date.now();
  res.on('finish', () => {
    const endTime = Date.now();
    const duration = endTime - startTime;
    // Assuming cost calculation logic here
    const cost = calculateCost(duration);
    apiRequestCost.labels(req.path, req.method).set(cost);
    logCostToJSONL(req.path, req.method, cost);
  });
  next();
}

function calculateCost(duration) {
  // Placeholder for actual cost calculation logic
  return duration * 0.001; // Example: 1ms costs 0.001 units
}

function logCostToJSONL(endpoint, method, cost) {
  const logEntry = JSON.stringify({ endpoint, method, cost, timestamp: new Date().toISOString() });
  fs.appendFileSync('/opt/axentx/surrogate-1/logs/cost-logs.jsonl', `${logEntry}\n`);
}

// Apply middleware to track cost
app.use(trackApiRequestCost);

module.exports = app;

// Start the server
const port = process.env.PROMETHEUS_PORT || 3000;
app.listen(port, () => {
  console.log(`Prometheus exporter listening on port ${port}`);
});