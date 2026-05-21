const { ZScore } = require('simple-statistics');

class AnomalyDetection {
  constructor(threshold = 3, windowSize = 5, thresholdMultiplier = 3) {
    this.threshold = threshold;
    this.windowSize = windowSize;
    this.thresholdMultiplier = thresholdMultiplier;
    this.spendingData = [];
  }

  addDataPoint(amount) {
    this.spendingData.push(amount);
  }

  detectAnomaly() {
    if (this.spendingData.length < this.windowSize) {
      return false;
    }

    const zScores = this.spendingData.map((amount, index) => {
      const start = Math.max(0, index - this.windowSize);
      const window = this.spendingData.slice(start, index);
      if (window.length === 0) return 0; // Not enough history to compare

      const m = mean(window);
      const sd = stdDev(window);
      return ZScore(amount, window);
    });

    const anomalies = detectAnomalies(zScores, {
      thresholdMultiplier: this.thresholdMultiplier,
    });

    return anomalies;
  }

  setThreshold(threshold) {
    this.threshold = threshold;
  }

  setWindowSize(windowSize) {
    this.windowSize = windowSize;
  }

  setThresholdMultiplier(thresholdMultiplier) {
    this.thresholdMultiplier = thresholdMultiplier;
  }
}

function mean(arr) {
  if (arr.length === 0) return 0;
  const sum = arr.reduce((acc, val) => acc + val, 0);
  return sum / arr.length;
}

function stdDev(arr) {
  if (arr.length === 0) return 0;
  const m = mean(arr);
  const variance =
    arr.reduce((acc, val) => acc + Math.pow(val - m, 2), 0) / arr.length;
  return Math.sqrt(variance);
}

function detectAnomalies(data, options) {
  const anomalies = [];
  for (let i = 0; i < data.length; i++) {
    const threshold = mean(data.slice(0, i)) + options.thresholdMultiplier * stdDev(data.slice(0, i));
    if (Math.abs(data[i]) > threshold) {
      anomalies.push(i);
    }
  }
  return anomalies;
}

module.exports = AnomalyDetection;