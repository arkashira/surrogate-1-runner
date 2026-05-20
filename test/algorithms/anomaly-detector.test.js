const anomalyDetector = require('./anomaly-detector');

describe('anomalyDetector', () => {
  it('should detect anomaly when data is outside threshold', () => {
    const data = [1, 2, 3, 4, 5, 100];
    const threshold = 2;
    const result = anomalyDetector(data, threshold);
    expect(result).toBe(true);
  });

  it('should not detect anomaly when data is within threshold', () => {
    const data = [1, 2, 3, 4, 5, 6];
    const threshold = 2;
    const result = anomalyDetector(data, threshold);
    expect(result).toBe(false);
  });
});