const config = require('../config/alerts');

function calculateAnomaly(currentCost) {
  // Placeholder for actual anomaly detection logic using historical data
  // This should compare the current cost against historical patterns
  // For simplicity, we're just checking if the current cost exceeds a fixed threshold
  const historicalAverage = 500; // Example average cost value
  const threshold = historicalAverage + (config.sigmaThreshold * 100); // Simplified calculation

  return currentCost > threshold;
}

module.exports = { calculateAnomaly };