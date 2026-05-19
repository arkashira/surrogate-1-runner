const { generateMetrics } = require('../src/generator/utils');

describe('generateMetrics', () => {
  it('should generate 10 metrics', () => {
    const metrics = generateMetrics('basic');
    expect(metrics.length).toBe(10);
  });

  it('should generate metrics with fixed names and values', () => {
    const metrics = generateMetrics('basic');
    expect(metrics[0].name).toBe('metric-0');
    expect(metrics[0].value).toBeLessThan(100);
  });

  it('should generate identical metrics when run twice', () => {
    const metrics1 = generateMetrics('basic');
    const metrics2 = generateMetrics('basic');
    expect(JSON.stringify(metrics1)).toBe(JSON.stringify(metrics2));
  });
});