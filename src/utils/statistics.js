/**
 * Statistical utility functions for anomaly detection
 */

function zScore(data, point) {
  if (data.length === 0) return 0;

  const mean = data.reduce((sum, d) => sum + d.amount, 0) / data.length;
  const variance = data.reduce((sum, d) => sum + Math.pow(d.amount - mean, 2), 0) / data.length;
  const stddev = Math.sqrt(variance);

  return (point.amount - mean) / stddev;
}

function rollingStats(data, window) {
  const stats = [];
  for (let i = 0; i < data.length; i++) {
    const slice = data.slice(Math.max(0, i - window + 1), i + 1);
    const mean = slice.reduce((sum, d) => sum + d.amount, 0) / slice.length;
    const variance =
      slice.reduce((sum, d) => sum + Math.pow(d.amount - mean, 2), 0) /
      slice.length;
    const stddev = Math.sqrt(variance);
    stats.push({ mean, stddev });
  }
  return stats;
}

module.exports = { zScore, rollingStats };