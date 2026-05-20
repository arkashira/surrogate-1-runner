const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

function costCalculatorMiddleware(req, res, next) {
  const startTime = performance.now();
  const requestId = uuidv4();

  // Simulate cost calculation (replace this with actual cost calculation logic)
  const cost = Math.floor(Math.random() * 100);

  res.on('finish', () => {
    const endTime = performance.now();
    const duration = endTime - startTime;

    // Write cost metadata to API response
    res.locals.cost = {
      id: requestId,
      duration: duration.toFixed(2),
      cost: cost,
    };

    // Write cost tracking to log file
    const logEntry = {
      id: requestId,
      timestamp: new Date().toISOString(),
      duration: duration.toFixed(2),
      cost: cost,
    };
    fs.appendFileSync('/opt/axentx/surrogate-1/logs/cost-logs.jsonl', JSON.stringify(logEntry) + '\n');
  });

  next();
}

module.exports = costCalculatorMiddleware;