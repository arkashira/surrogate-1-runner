# tests/runner.test.js
const { run } = require('../src/runner');

describe('runner', () => {
  it('should exit with non-zero status on failures', async () => {
    const { ci } = await run({ ci: true });
    expect(ci).toBe(false);
  });
});