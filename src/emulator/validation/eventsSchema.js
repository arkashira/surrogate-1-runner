const { z } = require('zod');

/**
 * Datadog Events API Schema Validator
 * Validates incoming events against Datadog-compatible schema
 * and normalizes timestamps to UTC.
 */

// Datadog event schema definition
const datadogEventSchema = z.object({
  // Required fields
  date: z.string().datetime().or(z.string().regex(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/)),
  message: z.string().min(1).max(10000),
  source: z.string().min(1).max(100),
  host: z.string().min(1).max(256),

  // Optional fields
  hostname: z.string().max(256).optional(),
  priority: z.enum(['info', 'error', 'warning', 'debug']).optional(),
  aggregation_key: z.string().max(256).optional(),
  alert_type: z.enum(['alert', 'metric', 'log']).optional(),
  metrics: z.array(z.object({
    metric: z.string().max(256),
    points: z.array(z.number()),
    type: z.enum(['gauge', 'count', 'histogram', 'set', 'distribution']),
  })).optional(),
  error_message: z.string().max(10000).optional(),
  error_type: z.string().max(256).optional(),
  request_id: z.string().max(256).optional(),
  tags: z.array(z.string().max(100)).optional(),
  dd: z.object({
    source: z.string().max(100).optional(),
    hostname: z.string().max(256).optional(),
    agent_version: z.string().max(16).optional(),
    lang: z.string().max(16).optional(),
    version: z.string().max(16).optional(),
  }).optional(),
});

/**
 * Normalize timestamp to UTC ISO 8601 format
 */
function normalizeTimestamp(timestamp) {
  const date = new Date(timestamp);
  if (isNaN(date.getTime())) {
    throw new Error(`Invalid timestamp: ${timestamp}`);
  }
  return date.toISOString();
}

/**
 * Validate event payload against Datadog schema
 * @param {Object} event - The event payload to validate
 * @returns {Object} - Validation result with success/error
 */
function validateEvent(event) {
  const result = {
    valid: false,
    errors: [],
    normalizedEvent: null,
  };

  try {
    // Deep clone to avoid mutating original
    const eventCopy = JSON.parse(JSON.stringify(event));
    
    // Validate against schema
    const validation = datadogEventSchema.safeParse(eventCopy);
    
    if (!validation.success) {
      result.errors = validation.error.errors.map(err => ({
        field: err.path.join('.'),
        message: err.message,
      }));
      return result;
    }

    // Normalize timestamp to UTC
    if (eventCopy.date) {
      eventCopy.date = normalizeTimestamp(eventCopy.date);
    }

    // Set default priority if not provided
    if (eventCopy.priority === undefined) {
      eventCopy.priority = 'info';
    }

    result.valid = true;
    result.normalizedEvent = eventCopy;
    return result;
  } catch (error) {
    result.errors.push({
      field: 'payload',
      message: `Validation failed: ${error.message}`,
    });
    return result;
  }
}

/**
 * Validate event and return Datadog-compatible error response
 * @param {Object} event - The event payload
 * @returns {Object} - Datadog-style error response
 */
function validateEventForResponse(event) {
  const result = validateEvent(event);
  
  if (!result.valid) {
    return {
      status: 400,
      errors: result.errors.map(err => ({
        field: err.field,
        message: err.message,
      })),
    };
  }

  return {
    status: 202,
    event: result.normalizedEvent,
  };
}

module.exports = {
  datadogEventSchema,
  validateEvent,
  validateEventForResponse,
  normalizeTimestamp,
};