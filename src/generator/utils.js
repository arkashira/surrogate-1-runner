const crypto = require('crypto');
const seed = 'surrogate-1-metrics-seed';

function generateMetrics(profile) {
  const hash = crypto.createHash('sha256');
  hash.update(seed);
  const deterministicSeed = hash.digest('hex').slice(0, 16);
  const metrics = [];

  for (let i = 0; i < 10; i++) {
    const metric = {
      name: `metric-${i}`,
      value: Math.floor(Math.random() * 100),
    };
    metrics.push(metric);
  }

  return metrics;
}

module.exports = { generateMetrics };