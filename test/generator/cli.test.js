const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

describe('generate-metrics command', () => {
  it('should generate 10 metrics with fixed names and values', () => {
    const output = execSync('node /opt/axentx/surrogate-1/src/generator/cli.js generate-metrics --profile basic').toString();
    const metrics = JSON.parse(output);
    expect(metrics.length).toBe(10);
    expect(metrics[0].name).toBe('metric1');
    expect(metrics[0].value).toBe(100);
  });

  it('should produce identical output when run twice', () => {
    const output1 = execSync('node /opt/axentx/surrogate-1/src/generator/cli.js generate-metrics --profile basic').toString();
    const output2 = execSync('node /opt/axentx/surrogate-1/src/generator/cli.js generate-metrics --profile basic').toString();
    expect(output1).toBe(output2);
  });

  it('should save metrics to metrics.json', () => {
    execSync('node /opt/axentx/surrogate-1/src/generator/cli.js generate-metrics --profile basic');
    const metricsPath = path.join(__dirname, '../src/generator/metrics.json');
    expect(fs.existsSync(metricsPath)).toBe(true);
    const metrics = JSON.parse(fs.readFileSync(metricsPath, 'utf8'));
    expect(metrics.length).toBe(10);
  });
});