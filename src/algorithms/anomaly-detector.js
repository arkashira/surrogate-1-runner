const calculateMean = (data) => data.reduce((a, b) => a + b, 0) / data.length;
const calculateStdDev = (data, mean) => Math.sqrt(data.map((x) => Math.pow(x - mean, 2)).reduce((a, b) => a + b, 0) / data.length);
const detectAnomaly = (data, threshold, mean, stdDev) => data.some((x) => Math.abs(x - mean) > threshold * stdDev);

module.exports = (data, threshold) => {
  const mean = calculateMean(data);
  const stdDev = calculateStdDev(data, mean);
  return detectAnomaly(data, threshold, mean, stdDev);
};