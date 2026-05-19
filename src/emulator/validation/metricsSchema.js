/**
 * Joi schema that mirrors Datadog's /api/v1/series payload.
 *
 * Required fields:
 *   - series: array of objects
 *   - each object must contain:
 *       * metric (string)
 *       * points (array of [timestamp, value] where both are numbers)
 *       * type   (one of "gauge", "count", "rate", "delta")
 *
 * Optional fields (allowed but not required):
 *   - host, device, tags, interval, unit, resources, meta, etc.
 *
 * The schema is deliberately strict on the required parts so that
 * we can return the same error shape Datadog does.
 */
const Joi = require('joi');

// Helper for a single point: [timestamp, value]
const pointSchema = Joi.array()
  .ordered(
    Joi.number().required().label('timestamp'), // Unix epoch seconds (or ms)
    Joi.number().required().label('value')
  )
  .length(2)
  .required();

const seriesItemSchema = Joi.object({
  metric: Joi.string().trim().required(),
  points: Joi.array().items(pointSchema).min(1).required(),
  type: Joi.string()
    .valid('gauge', 'count', 'rate', 'delta')
    .required(),

  // ---- optional fields (Datadog permits them) ----
  host: Joi.string().allow(null, ''),
  device: Joi.string().allow(null, ''),
  tags: Joi.array().items(Joi.string()).allow(null),
  interval: Joi.number().positive().allow(null),
  unit: Joi.string().allow(null),
  resources: Joi.array().items(Joi.object()).allow(null),
  meta: Joi.object().allow(null)
}).required();

const metricsSchema = Joi.object({
  series: Joi.array().items(seriesItemSchema).min(1).required()
}).required();

module.exports = {
  /** Validate a raw payload and return {error, value}. */
  validateSeriesPayload: (payload) => metricsSchema.validate(payload, { abortEarly: false })
};