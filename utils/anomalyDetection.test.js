const AnomalyDetection = require('./anomalyDetection');

describe('AnomalyDetection', () => {
  let anomalyDetection;

  beforeEach(() => {
    anomalyDetection = new AnomalyDetection();
  });

  test('should not detect anomaly with insufficient data', () => {
    anomalyDetection.addDataPoint(100);
    expect(anomalyDetection.detectAnomaly()).toBe(false);
  });

  test('should detect anomaly when spending exceeds threshold', () => {
    for (let i = 0; i < 30; i++) {
      anomalyDetection.addDataPoint(100);
    }
    anomalyDetection.addDataPoint(500);
    expect(anomalyDetection.detectAnomaly()).toBe(true);
  });

  test('should not detect anomaly when spending is within threshold', () => {
    for (let i = 0; i < 30; i++) {
      anomalyDetection.addDataPoint(100);
    }
    anomalyDetection.addDataPoint(150);
    expect(anomalyDetection.detectAnomaly()).toBe(false);
  });

  test('should update threshold', () => {
    anomalyDetection.setThreshold(4);
    expect(anomalyDetection.threshold).toBe(4);
  });

  test('should update window size', () => {
    anomalyDetection.setWindowSize(10);
    expect(anomalyDetection.windowSize).toBe(10);
  });

  test('should update threshold multiplier', () => {
    anomalyDetection.setThresholdMultiplier(2);
    expect(anomalyDetection.thresholdMultiplier).toBe(2);
  });
});