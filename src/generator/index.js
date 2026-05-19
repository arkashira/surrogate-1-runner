const { generateMetrics } = require('./utils');

function generateMetricsCLI(profile) {
  const metrics = generateMetrics(profile);
  console.log(JSON.stringify(metrics, null, 2));
}

module.exports = { generateMetricsCLI };