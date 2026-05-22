const { fetchPerformanceBenchmarks, updatePerformanceBenchmarks } = require('../api/performanceBenchmarkApi');

let benchmarksCache = null;
let lastUpdated = null;

const getCachedBenchmarks = () => {
  return benchmarksCache;
};

const isCacheStale = () => {
  if (!lastUpdated) return true;
  const now = new Date();
  const diffMinutes = (now - lastUpdated) / (1000 * 60);
  return diffMinutes > 30; // Cache expires after 30 minutes
};

const refreshBenchmarks = async () => {
  try {
    const updatedBenchmarks = await updatePerformanceBenchmarks();
    benchmarksCache = updatedBenchmarks;
    lastUpdated = new Date();
    return benchmarksCache;
  } catch (error) {
    console.error('Error refreshing benchmarks:', error);
    throw error;
  }
};

const getPerformanceBenchmarks = async () => {
  if (isCacheStale()) {
    return refreshBenchmarks();
  }
  return getCachedBenchmarks();
};

module.exports = {
  getPerformanceBenchmarks,
  refreshBenchmarks,
  getCachedBenchmarks,
};