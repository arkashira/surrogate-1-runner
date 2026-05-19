const express = require('express');
const { validateEventForResponse } = require('../validation/eventsSchema');

const router = express.Router();

/**
 * POST /api/v1/events
 * Accepts Datadog-compatible event payloads
 * Returns HTTP 202 with normalized event or HTTP 400 with validation errors
 */
router.post('/', (req, res) => {
  const event = req.body;

  if (!event || typeof event !== 'object') {
    return res.status(400).json({
      status: 400,
      errors: [{
        field: 'payload',
        message: 'Event payload must be a non-empty object',
      }],
    });
  }

  const result = validateEventForResponse(event);

  if (result.status === 400) {
    return res.status(400).json(result);
  }

  res.status(202).json(result);
});

module.exports = router;