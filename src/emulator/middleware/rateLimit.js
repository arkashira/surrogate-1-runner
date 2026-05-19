const rateLimit = require('express-rate-limit');

const createRateLimiter = (maxRequests = 1200, windowMs = 3600000) => {
  return rateLimit({
    windowMs, // Time window in milliseconds
    max: maxRequests, // Max requests per window
    standardHeaders: true, // Return rate limit info in `RateLimit-*` headers
    legacyHeaders: false, // Disable `X-RateLimit-*` headers
    message: {
      errors: [
        {
          message: 'API rate limit exceeded',
        }
      ]
    },
    // Explicitly count all requests (success and failure) against the limit
    skipSuccessfulRequests: false,
    skipFailedRequests: false,
    // Custom handler to ensure consistent JSON error structure
    handler: (req, res, next, options) => {
      res.status(options.statusCode).json({
        errors: [
          {
            message: 'API rate limit exceeded',
          }
        ]
      });
    }
  });
};

module.exports = {
  createRateLimiter
};