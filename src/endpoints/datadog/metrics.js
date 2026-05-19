const express = require('express');
const router = express.Router();

/**
 * Validate required headers:
 * - DD-API-KEY must be present and non-empty
 * - Content-Type must be application/json
 */
function validateHeaders(req, res, next) {
  const apiKey = req.header('DD-API-KEY');
  const contentType = req.header('Content-Type');

  if (!apiKey) {
    return res.status(403).json({ errors: [{ title: 'Missing API key' }] });
  }
  if (!contentType || !contentType.includes('application/json')) {
    return res.status(415).json({ errors: [{ title: 'Unsupported Media Type' }] });
  }
  next();
}

/**
 * Generate a synthetic Datadog-style metric payload.
 * The shape mirrors Datadog's /api/v2/metrics ingestion format.
 */
function buildResponseBody(metricName, value) {
  const timestamp = Math.floor(Date.now() / 1000); // seconds since epoch
  return {
    data: [
      {
        type: 'metric_series',
        id: `mock-${timestamp}`,
        attributes: {
          metric: metricName,
          points: [[timestamp, value]],
          tags: [],
          host: 'mock-host',
          interval: 60
        }
      }
    ]
  };
}

/**
 * POST /api/v2/metrics
 * Expected body: { metric: string, tags: array, host: string, interval: number }
 * The mock simply echoes back a synthetic series confirming receipt.
 */
router.post('/api/v2/metrics', validateHeaders, (req, res) => {
  // Basic payload sanity check – ensure a JSON body exists
  if (!req.body || typeof req.body !== 'object') {
    return res.status(400).json({ errors: [{ title: 'Invalid JSON payload' }] });
  }

  // Use the metric name from the request for the response (or fallback)
  const incomingMetric = req.body.metric || 'mock.metric';
  const syntheticValue = Math.random() * 100; // generate a dummy value

  const responseBody = buildResponseBody(incomingMetric, syntheticValue);
  res.status(200).json(responseBody);
});

module.exports = router;