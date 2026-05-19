const express = require('express');
const router = express.Router();
const { rateLimiter } = require('../middleware/rateLimit');

// Mock rate limit configuration
const MAX_REQUESTS_PER_HOUR = 1000;
const RATE_LIMIT_WINDOW_MS = 60 * 60 * 1000; // 1 hour

// In-memory storage for rate limiting (in production, use Redis or similar)
const requestCounts = new Map();

function checkRateLimit(req, res, next) {
  const clientIP = req.ip || req.connection.remoteAddress;
  const now = Date.now();
  
  if (!requestCounts.has(clientIP)) {
    requestCounts.set(clientIP, []);
  }
  
  const clientRequests = requestCounts.get(clientIP);
  
  // Remove requests older than the window
  const validRequests = clientRequests.filter(timestamp => 
    now - timestamp < RATE_LIMIT_WINDOW_MS
  );
  
  // Update the count
  requestCounts.set(clientIP, [...validRequests, now]);
  
  if (validRequests.length >= MAX_REQUESTS_PER_HOUR) {
    return res.status(429).json({
      error: {
        message: "Rate limit exceeded"
      }
    });
  }
  
  next();
}

router.post('/api/v1/series', 
  rateLimiter,
  checkRateLimit,
  (req, res) => {
    // Validate request body
    if (!req.body || !Array.isArray(req.body.series)) {
      return res.status(400).json({
        error: {
          message: "Invalid payload format"
        }
      });
    }

    // Process series data (mock implementation)
    const seriesData = req.body.series;
    
    // Simulate processing time
    setTimeout(() => {
      // Return success response matching Datadog's format
      res.status(202).json({
        status: "ok"
      }).set({
        'X-RateLimit-Limit': MAX_REQUESTS_PER_HOUR.toString(),
        'X-RateLimit-Remaining': (MAX_REQUESTS_PER_HOUR - requestCounts.get(req.ip || req.connection.remoteAddress).length).toString()
      });
    }, 10);
  }
);

module.exports = router;