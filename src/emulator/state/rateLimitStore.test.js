const RateLimitStore = require('./rateLimitStore');

describe('RateLimitStore', () => {
  let store;

  beforeEach(() => {
    store = new RateLimitStore(5, 60000);
  });

  test('allows requests within quota', () => {
    for (let i = 0; i < 5; i++) {
      const result = store.check('test-key');
      expect(result.allowed).toBe(true);
    }
  });

  test('blocks requests exceeding quota', () => {
    for (let i = 0; i < 5; i++) {
      store.check('test-key');
    }
    const result = store.check('test-key');
    expect(result.allowed).toBe(false);
    expect(result.retryAfter).toBeGreaterThan(0);
  });

  test('resets quota after window elapses', () => {
    for (let i = 0; i < 5; i++) {
      store.check('test-key');
    }
    
    jest.useFakeTimers().setSystemTime(Date.now() + 60000);
    const result = store.check('test-key');
    expect(result.allowed).toBe(true);
  });

  test('scopes quotas per API key', () => {
    for (let i = 0; i < 5; i++) {
      store.check('key1');
    }
    const result1 = store.check('key1');
    expect(result1.allowed).toBe(false);

    const result2 = store.check('key2');
    expect(result2.allowed).toBe(true);
  });

  test('provides correct retryAfter time', () => {
    for (let i = 0; i < 5; i++) {
      store.check('test-key');
    }
    
    const startTime = Date.now();
    jest.useFakeTimers().setSystemTime(startTime + 30000);
    const result = store.check('test-key');
    expect(result.retryAfter).toBeCloseTo(30, 0);
  });
});