const { ValidationError } = require('http-errors');

exports.validateMetricsArray = (metrics) => {
  if (!Array.isArray(metrics)) {
    throw new ValidationError('Metrics must be an array.');
  }

  metrics.forEach((metric, i) => {
    if (typeof metric.name !== 'string' || !metric.name.trim()) {
      throw new ValidationError(`Metric #${i + 1} is missing a valid name.`);
    }
    if (typeof metric.unit !== 'string' || !metric.unit.trim()) {
      throw new ValidationError(`Metric #${i + 1} is missing a valid unit.`);
    }
    if (typeof metric.target !== 'number' || !Number.isFinite(metric.target)) {
      throw new ValidationError(`Metric #${i + 1} has an invalid target.`);
    }
    if (metric.target < 0) {
      throw new ValidationError(`Metric #${i + 1} target must be non‑negative.`);
    }
    if (metric.timeframe && typeof metric.timeframe !== 'string') {
      throw new ValidationError(`Metric #${i + 1} timeframe must be a string.`);
    }
  });
};

exports.validateCreateValidationProject = (data) => {
  // Existing validations go here…

  if (data.metrics) {
    exports.validateMetricsArray(data.metrics);
  }
};

exports.validateUpdateValidationProject = (data) => {
  // Existing validations go here…

  if (data.metrics) {
    exports.validateMetricsArray(data.metrics);
  }
};